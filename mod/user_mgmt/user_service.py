from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException
from mod.user_mgmt.UserDTO import UserCreateDTO, UserUpdateDTO, UserResponseDTO
from mod.user_mgmt.user_repository import user_repository
from mod.user_mgmt.UserModel import UserRole, UserStatus
from mod.user_mgmt.helpers.paswtool import get_password_hash, generate_random_password

class UserService:
    """
    Service layer for user management operations.

    This service provides business logic for user CRUD operations, including:
    - User creation with validation and smart defaults
    - User retrieval with filtering, searching, and pagination
    - User updates with uniqueness validation
    - User deletion
    - User status toggling

    The service layer sits between the controller (API routes) and repository (data access),
    handling business rules, validation, and data transformation.

    Attributes:
        user_repository: Instance of UserRepository for database operations
    """

    def __init__(self):
        """Initialize UserService with user repository instance."""
        self.user_repository = user_repository
    
    def create_user(self, db: Session, user: UserCreateDTO) -> UserResponseDTO:
        """
        Create a new user with business logic validation and smart defaults.
        
        This method handles the complete user creation process including:
        - Validating email and username uniqueness
        - Generating a random 6-character password if not provided
        - Applying default role (User) and status (Active) if not specified
        - Hashing the password before storage for security

        Args:
            db (Session): SQLAlchemy database session for transaction management
            user (UserCreateDTO): Data transfer object containing user information
                Required fields:
                    - username: Unique username (6-50 characters)
                    - email: Unique email address
                Optional fields with defaults:
                    - password: User password (auto-generated if not provided)
                    - role: User role (defaults to 'User')
                    - status: Account status (defaults to 'Active')
                    - first_name, last_name, job_title: Additional user info

        Returns:
            UserResponseDTO: Data transfer object containing the created user's information
                (excluding sensitive data like password)

        Raises:
            HTTPException: 400 if email already registered
            HTTPException: 400 if username already taken

        Example:
            >>> user_data = UserCreateDTO(
            ...     username="johndoe123",
            ...     email="john@example.com",
            ...     first_name="John",
            ...     last_name="Doe"
            ... )
            >>> new_user = user_service.create_user(db, user_data)
            >>> print(new_user.username)  # "johndoe123"

        Note:
            When password is auto-generated, in a production system you should:
            - Log the generated password securely
            - Send it to the user via email
            - Require password change on first login
        """
        # Check if user with email already exists
        existing_user = self.user_repository.get_user_by_email(db, email=user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if username already exists
        existing_username = self.user_repository.get_user_by_username(db, username=user.username)
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        # Prepare user data with defaults
        user_data = user.model_dump()
        
        # Generate random password if not provided
        if not user.password:
            generated_password = generate_random_password(6)
            user_data['password'] = get_password_hash(generated_password)
            # Note: In a real system, you might want to return the generated password 
            # or send it via email to the user
        else:
            # Hash the provided password
            user_data['password'] = get_password_hash(user.password)
        
        # Ensure defaults are set (though they should be set by Pydantic already)
        if user_data.get('role') is None:
            user_data['role'] = 'User'
        if user_data.get('status') is None:
            user_data['status'] = 'Active'
        
        new_user = self.user_repository.create_user(db=db, user_data=user_data)
        return UserResponseDTO.model_validate(new_user)
    
    def get_user_by_id(self, db: Session, user_id: int) -> UserResponseDTO:
        """
        Retrieve a specific user by their unique identifier.

        This method fetches a single user's complete information from the database
        using their unique ID. It's commonly used for:
        - Displaying user profile pages
        - Retrieving user data before updates
        - Verifying user existence
        - Admin user management operations

        Args:
            db (Session): SQLAlchemy database session for query execution
            user_id (int): The unique integer identifier of the user to retrieve
                Must be a positive integer corresponding to an existing user

        Returns:
            UserResponseDTO: Data transfer object containing complete user information
                including all profile fields except sensitive data (password)

        Raises:
            HTTPException: 404 if user with the given ID does not exist

        Example:
            >>> user = user_service.get_user_by_id(db, user_id=1)
            >>> print(f"{user.first_name} {user.last_name}")  # "John Doe"
            >>> print(user.email)  # "john@example.com"

        Note:
            This method does not perform any authentication or authorization checks.
            Ensure proper access control is implemented at the controller/route level.
        """
        user = self.user_repository.get_user_by_id(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponseDTO.model_validate(user)
    
    def get_users(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        search_term: Optional[str] = None,
        status: Optional[UserStatus] = None,
        role: Optional[UserRole] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> List[UserResponseDTO]:
        """
        Retrieve a list of users with comprehensive filtering, searching, and pagination.

        This method provides powerful querying capabilities for user listings:
        - Pagination support for efficient data loading
        - Full-text search across multiple fields
        - Filtering by user status and role
        - Flexible sorting by any user field
        - Returns sanitized user data (passwords excluded)

        Args:
            db (Session): SQLAlchemy database session for query execution
            skip (int, optional): Number of records to skip for pagination.
                Defaults to 0. Use with limit for implementing page navigation.
            limit (int, optional): Maximum number of records to return.
                Defaults to 100. Maximum allowed is typically 1000.
            search_term (Optional[str], optional): Search query for filtering users.
                Searches across first_name, last_name, email, and username fields
                using case-insensitive partial matching. Defaults to None (no search).
            status (Optional[UserStatus], optional): Filter users by account status.
                Valid values: UserStatus.ACTIVE, UserStatus.INACTIVE.
                Defaults to None (all statuses included).
            role (Optional[UserRole], optional): Filter users by role.
                Valid values: UserRole.ADMIN, UserRole.USER, UserRole.MODERATOR.
                Defaults to None (all roles included).
            sort_by (str, optional): Field name to sort results by.
                Valid fields: "id", "username", "email", "first_name", "last_name",
                "created_at", "updated_at". Defaults to "created_at".
            sort_order (str, optional): Sort direction, either "asc" (ascending) or
                "desc" (descending). Defaults to "desc" (newest first).

        Returns:
            List[UserResponseDTO]: List of user data transfer objects matching the criteria.
                Returns empty list if no users match the filters.
                Each DTO contains complete user info excluding sensitive fields.

        Examples:
            >>> # Get first 20 users (newest first)
            >>> users = user_service.get_users(db, limit=20)

            >>> # Search for users with "engineer" in their info
            >>> engineers = user_service.get_users(db, search_term="engineer")

            >>> # Get active admin users, sorted by name
            >>> admins = user_service.get_users(
            ...     db,
            ...     status=UserStatus.ACTIVE,
            ...     role=UserRole.ADMIN,
            ...     sort_by="last_name",
            ...     sort_order="asc"
            ... )

            >>> # Pagination: get second page (users 21-40)
            >>> page_2 = user_service.get_users(db, skip=20, limit=20)

        Note:
            - Search is case-insensitive and uses partial matching (LIKE '%term%')
            - Multiple filters are combined with AND logic
            - Results are always sanitized to exclude password hashes
            - For large datasets, consider adding caching at the controller level
        """
        users = self.user_repository.get_users(
            db=db,
            skip=skip,
            limit=limit,
            search_term=search_term,
            status=status,
            role=role,
            sort_by=sort_by,
            sort_order=sort_order
        )
        return [UserResponseDTO.model_validate(user) for user in users]
    
    def update_user(self, db: Session, user_id: int, user_update: UserUpdateDTO) -> UserResponseDTO:
        """
        Update an existing user's information with validation and security checks.

        This method handles partial updates to user records with comprehensive validation:
        - Verifies user existence before updating
        - Validates email uniqueness (if being changed)
        - Validates username uniqueness (if being changed)
        - Automatically hashes new passwords for security
        - Only updates fields that are provided (partial updates)
        - Updates the updated_at timestamp automatically

        Args:
            db (Session): SQLAlchemy database session for transaction management
            user_id (int): The unique identifier of the user to update
            user_update (UserUpdateDTO): Data transfer object containing fields to update
                All fields are optional - only provided fields will be updated:
                    - username: New username (must be unique)
                    - email: New email address (must be unique)
                    - password: New password (will be hashed automatically)
                    - first_name, last_name: Updated personal information
                    - job_title: Updated professional information
                    - role: Updated user role (Admin, User, Moderator)
                    - status: Updated account status (Active, Inactive, Pending)

        Returns:
            UserResponseDTO: Data transfer object containing the updated user's complete
                information with all current field values and updated timestamp

        Raises:
            HTTPException: 404 if user with the given ID does not exist
            HTTPException: 400 if new email is already registered by another user
            HTTPException: 400 if new username is already taken by another user

        Examples:
            >>> # Update user's name and job title
            >>> update_data = UserUpdateDTO(
            ...     first_name="Jonathan",
            ...     last_name="Doe-Smith",
            ...     job_title="Senior Software Engineer"
            ... )
            >>> updated_user = user_service.update_user(db, user_id=1, user_update=update_data)

            >>> # Change user's password
            >>> password_update = UserUpdateDTO(password="newSecurePassword123")
            >>> user_service.update_user(db, user_id=1, user_update=password_update)

            >>> # Promote user to admin
            >>> role_update = UserUpdateDTO(role=UserRole.ADMIN)
            >>> user_service.update_user(db, user_id=1, user_update=role_update)

            >>> # Deactivate user account
            >>> status_update = UserUpdateDTO(status=UserStatus.INACTIVE)
            >>> user_service.update_user(db, user_id=1, user_update=status_update)

        Note:
            - Password changes are automatically hashed using bcrypt
            - Email and username uniqueness is checked only when those fields are being updated
            - The method uses exclude_unset=True to only update provided fields
            - Validation errors from the DTO are handled by FastAPI/Pydantic automatically
            - Consider logging sensitive operations like role changes for audit purposes
        """
        # Check if user exists
        existing_user = self.user_repository.get_user_by_id(db, user_id=user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if email is being updated and if it's already taken by another user
        if user_update.email:
            email_user = self.user_repository.get_user_by_email(db, email=user_update.email)
            if email_user and email_user.id != user_id:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if username is being updated and if it's already taken by another user
        if user_update.username:
            username_user = self.user_repository.get_user_by_username(db, username=user_update.username)
            if username_user and username_user.id != user_id:
                raise HTTPException(status_code=400, detail="Username already taken")
        
        # Hash password if it's being updated
        user_data = user_update.model_dump(exclude_unset=True)
        if 'password' in user_data and user_data['password']:
            user_data['password'] = get_password_hash(user_data['password'])
        
        updated_user = self.user_repository.update_user(db=db, user_id=user_id, user_data=user_data)
        return UserResponseDTO.model_validate(updated_user)
    
    def delete_user(self, db: Session, user_id: int) -> dict:
        """
        Permanently delete a user from the system.

        ⚠️ WARNING: This operation is IRREVERSIBLE and permanently removes all user data.

        This method performs hard deletion of a user record from the database.
        Once deleted:
        - All user data is permanently lost
        - The user cannot log in anymore
        - The user ID cannot be reused
        - Any foreign key references may become orphaned

        Consider using status updates (setting to INACTIVE) instead of deletion
        if you need to preserve user data or maintain referential integrity.

        Args:
            db (Session): SQLAlchemy database session for transaction management
            user_id (int): The unique identifier of the user to permanently delete

        Returns:
            dict: Success confirmation message
                Format: {"message": "User deleted successfully"}

        Raises:
            HTTPException: 404 if user with the given ID does not exist

        Examples:
            >>> # Delete a test user
            >>> result = user_service.delete_user(db, user_id=999)
            >>> print(result)  # {"message": "User deleted successfully"}

            >>> # Better alternative: Deactivate instead of delete
            >>> update_data = UserUpdateDTO(status=UserStatus.INACTIVE)
            >>> user_service.update_user(db, user_id=1, user_update=update_data)

        Best Practices:
            1. **Verify Authorization**: Ensure the requester has proper permissions
            2. **Backup Data**: Export important user data before deletion
            3. **Check Dependencies**: Verify no critical data depends on this user
            4. **Consider Soft Delete**: Use status=INACTIVE instead when possible
            5. **Audit Logging**: Log deletion operations for compliance and audit trails
            6. **Cascade Effects**: Be aware of cascade deletes on related records

        Use Cases:
            - Removing test/demo accounts from development environments
            - Cleaning up spam or fake accounts
            - Fulfilling GDPR "right to be forgotten" requests
            - Removing accounts that violated terms of service
            - System maintenance with proper backups in place

        Inappropriate Use Cases:
            - Temporary user suspension (use status update instead)
            - Regular user management (prefer deactivation)
            - When user data might be needed for historical records
            - When foreign key relationships need to be preserved

        Note:
            After deletion, the HTTP response should return 204 No Content
            at the controller level to indicate successful deletion with no body.
        """
        success = self.user_repository.delete_user(db=db, user_id=user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"message": "User deleted successfully"}

    def toggle_user_status(self, db: Session, user_id: int) -> UserResponseDTO:
        """
        Toggle a user's account status between ACTIVE and INACTIVE.

        This is a convenience method for quickly enabling or disabling user accounts
        without needing to specify the target status explicitly. It automatically
        determines the opposite status and applies it.

        Status Toggle Rules:
        - If current status is ACTIVE → changes to INACTIVE (disable account)
        - If current status is INACTIVE → changes to ACTIVE (enable account)

        This operation is commonly used for:
        - Quick user account suspension/reactivation
        - Administrative user management
        - Implementing account ban/unban features
        - Temporarily disabling problematic accounts

        Args:
            db (Session): SQLAlchemy database session for transaction management
            user_id (int): The unique identifier of the user whose status to toggle

        Returns:
            UserResponseDTO: Data transfer object containing the updated user information
                with the new status reflected

        Raises:
            HTTPException: 404 if user with the given ID does not exist
            HTTPException: 500 if database error occurs during the operation
                (database is automatically rolled back on error)

        Examples:
            >>> # Deactivate an active user
            >>> user = user_service.get_user_by_id(db, user_id=1)
            >>> print(user.status)  # UserStatus.ACTIVE
            >>> updated = user_service.toggle_user_status(db, user_id=1)
            >>> print(updated.status)  # UserStatus.INACTIVE

            >>> # Reactivate the same user
            >>> updated_again = user_service.toggle_user_status(db, user_id=1)
            >>> print(updated_again.status)  # UserStatus.ACTIVE

        Process Flow:
            1. Retrieve user from database by ID
            2. Check if user exists (raise 404 if not)
            3. Determine opposite status (ACTIVE ↔ INACTIVE)
            4. Update user status in database
            5. Commit transaction to database
            6. Refresh user object with new values
            7. Return updated user data
            8. On any error: rollback transaction and raise 500

        Note:
            - This method handles its own transaction management (commit/rollback)
            - All status changes are logged for audit purposes
            - The operation is atomic - either fully succeeds or fully fails
            - Consider adding additional checks for business rules (e.g., can't deactivate admin)
            - May want to trigger notifications when user status changes

        Security Considerations:
            - Ensure proper authorization before allowing status toggles
            - Log all status changes for security auditing
            - Consider requiring reason/comment for deactivations
            - May want to prevent self-deactivation for admin users
        """
        import logging
        logger = logging.getLogger(__name__)
        user = self.user_repository.get_user_by_id(db, user_id=user_id)
        if not user:
            logger.warning(f"User with id {user_id} not found for status toggle.")
            raise HTTPException(status_code=404, detail="User not found")
        try:
            if user.status == UserStatus.ACTIVE:
                user.status = UserStatus.INACTIVE
            else:
                user.status = UserStatus.ACTIVE
            db.commit()
            db.refresh(user)
            logger.info(f"Toggled status for user {user_id} to {user.status}.")
            return UserResponseDTO.model_validate(user)
        except Exception as e:
            db.rollback()
            logger.error(f"Error toggling status for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

# Create instance
user_service = UserService()