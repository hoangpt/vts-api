# Prompt cho luồng Login

## Mô tả
Người dùng cần đăng nhập vào hệ thống để truy cập các chức năng.

## Yêu cầu
- Nhập tên đăng nhập (username) và mật khẩu (password).
- Kiểm tra thông tin đăng nhập hợp lệ.
- Nếu đăng nhập thành công, chuyển đến trang chính.
- Nếu đăng nhập thất bại, hiển thị thông báo lỗi.

## Prompt
Bạn hãy xây dựng luồng đăng nhập cho ứng dụng:
1. Hiển thị form yêu cầu nhập tên đăng nhập và mật khẩu.
2. Khi người dùng nhấn nút đăng nhập, kiểm tra thông tin hợp lệ.
3. Nếu đúng, chuyển sang giao diện chính của ứng dụng.
4. Nếu sai, hiển thị thông báo lỗi "Tên đăng nhập hoặc mật khẩu không đúng".
5. Còn 1 trường hợp nữa là đăng nhập đúng nhưng acc bị disable. Cũng cần thông báo cho case này nữa.

---

# Prompt cho luồng Logout

## Mô tả
Người dùng có thể đăng xuất khỏi hệ thống để đảm bảo an toàn.

## Yêu cầu
- Hiển thị nút hoặc tuỳ chọn đăng xuất.
- Khi người dùng chọn đăng xuất, kết thúc phiên làm việc.
- Chuyển về màn hình đăng nhập.

## Prompt
Bạn hãy xây dựng luồng đăng xuất cho ứng dụng:
1. Hiển thị nút hoặc tuỳ chọn đăng xuất trên giao diện chính.
2. Khi người dùng chọn đăng xuất, kết thúc phiên làm việc hiện tại.
3. Chuyển về màn hình đăng nhập.