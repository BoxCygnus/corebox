# 📦 COREBOX — Ứng Dụng Quản Lý Dự Án & Soát Mã Công Việc

> *"Your project management, minus the manual hassle."*  
> **Data storage, automated inspection, and other supportive tools.**  
> *Developed by Box*

---

## 🌟 Giới Thiệu Tổng Quan

**COREBOX** là nền tảng web hoàn chỉnh hỗ trợ Quản lý Dự án (QLDA), được xây dựng bằng **Python**, tích hợp mạng lưới đám mây **Cloudflare** (Cloudflare Tunnel, Cloudflare D1, Cloudflare Access) và mã nguồn mở trên **GitHub**. Ứng dụng có thể chạy cục bộ hoặc triển khai chia sẻ trực tiếp ra internet thông qua các tên miền miễn phí của Cloudflare (`trycloudflare.com`).

---

## 🚀 Các Tính Năng Trọng Tâm

### 1. Nhận Diện Thương Hiệu & Cấu Trúc Giao Diện
- **Top Navbar:**
  - Góc trái: `📦 Corebox` ➔ `Tools` (Dropdown) ➔ `Administrator` (Dropdown).
  - Góc phải: Công cụ chuyển đổi ngôn ngữ (**Tiếng Việt** / **English**) và biểu tượng tài khoản Google kèm trạng thái đăng nhập.
  - Bấm vào `📦 Corebox` quay về màn hình chính.
- **Màn hình chính (Main Dashboard):**
  - Tiêu đề **COREBOX** với hiệu ứng phát sáng lấp lánh (Glowing Shimmer Gradient).
  - Câu slogan & mô tả chính thức của hệ thống.
  - Chân trang ghi nhận bản quyền: *"Developed by Box"*.

### 2. Xác Thực, Phân Quyền & Hàng Đợi Phê Duyệt (Approval Queue)
- **Đăng nhập Google & Cloudflare Access:** Hỗ trợ nhận diện tự động qua HTTP Header `Cf-Access-Authenticated-User-Email` khi đứng sau Cloudflare Zero Trust Access, đồng thời tích hợp bộ chuyển tài khoản kiểm thử thông minh.
- **Admin chính thức:** `happyclone96@gmail.com` luôn mặc định có quyền Quản trị tối cao (`admin` & `active`).
- **Luồng phê duyệt tài khoản mới:** Người dùng mới đăng nhập lần đầu sẽ tự động lưu vào bảng `users` với trạng thái `pending`. Ứng dụng hiển thị thông báo chờ lịch sự:  
  > *"Tài khoản của bạn đã đăng nhập thành công nhưng đang chờ Admin (happyclone96@gmail.com) phê duyệt. Vui lòng liên hệ quản trị viên."*
- **Quản lý phân quyền (Admin Only):** Hiển thị hàng đợi tài khoản chờ duyệt với 2 nút hành động `[Phê duyệt]` và `[Từ chối]`. Chỉ tài khoản Admin mới có quyền truy cập mục này.

### 3. Kho Dữ Liệu Công Việc (Data Repository)
- **Trích xuất thông minh:** Tự động lọc bỏ các đoạn văn bản mô tả rườm rà từ tệp `.docx`, `.xlsx`, `.pdf` và chỉ trích xuất đúng bảng chứa Mã CV và Tên công việc.
- **Nhận diện cột linh hoạt:** Hỗ trợ mọi biến thể tên cột ("Mã hiệu", "Mã CV", "Mã định mức", "Tên công tác", "Nội dung công việc", "Công tác lắp đặt"...).
- **Quy chuẩn hóa Mã CV (XX.YYYYY):**
  - Định dạng chuẩn 2 chữ cái + dấu chấm + 5 chữ số.
  - Nếu mã nguồn có 1-4 chữ số (ví dụ: `AB.123` hoặc `AF.1234`), hệ thống **tự động đệm số 0 vào cuối cho đủ 5 chữ số** (`AB.12300`, `AF.12340`) trước khi lưu trữ vào Database / Cloudflare D1.
- **Quản lý danh mục:** Lưu trữ gắn thẻ `source_file`, cho phép xem toàn bộ danh mục tổng hợp, tìm kiếm thời gian thực, lọc và tải về file Excel. Chỉ Admin mới có quyền Tải lên hoặc Xóa dữ liệu.

### 4. Kiểm Tra Mã Công Việc (Work Code Inspection)
- **Bảo mật tạm thời:** Tệp tải lên để kiểm tra chỉ được xử lý trong bộ nhớ phiên làm việc (Session) và được giải phóng ngay sau đó, hoàn toàn không lưu trữ lâu dài trên server.
- **Quy tắc Sheet ĐGTH:** Chỉ kiểm tra trên sheet có tên chính xác là `ĐGTH` bằng thư viện `openpyxl` với tham số `data_only=True` để lấy giá trị thực từ công thức.
- **Phân nhóm theo Hạng mục công trình:** Dữ liệu trong sheet `ĐGTH` được chia thành từng bảng theo từng hạng mục và số thứ tự (STT) lặp lại từ 1. Hệ thống tự động chia và nhóm các mã lỗi theo đúng từng Hạng mục công trình.
- **Báo lỗi tức thì:** Nếu mã trong file không có trong kho dữ liệu, hệ thống gắn cờ lỗi ngay kèm số dòng và hiển thị gọn gàng trong các khối `st.expander` theo từng Hạng mục.
- **Xuất báo cáo:** Cho phép tải báo cáo đối soát chi tiết dạng file `.xlsx`.

---

## 🌐 Triển Khai Trực Tiếp Lên Tên Miền Miễn Phí `*.pages.dev` (Cloudflare Pages)

Ứng dụng **COREBOX** đã được đóng gói sẵn sàng để chạy trực tiếp trên nền tảng **Cloudflare Pages**, cho phép người dùng truy cập mọi lúc mọi nơi qua đường link dạng:
👉 **`https://<ten-du-an-cua-ban>.pages.dev`**  
*(Hoàn toàn miễn phí, có chứng chỉ SSL HTTPS, máy chủ chạy 24/7 không cần mở máy tính cá nhân).*

### Các Bước Triển Khai Qua GitHub:
1. **Đưa mã nguồn lên GitHub:**
   ```powershell
   git add .
   git commit -m "San sang cho Cloudflare Pages .pages.dev"
   git push origin main
   ```
2. **Kết nối Cloudflare Pages:**
   - Đăng nhập vào [Cloudflare Dashboard](https://dash.cloudflare.com/).
   - Vào mục **Workers & Pages** (hoặc **Compute**) ➔ Chọn tab **Pages** ➔ Bấm **Create application** ➔ **Connect to Git**.
   - Chọn kho GitHub của bạn (ví dụ: `corebox`).
3. **Cấu hình bản build:**
   - **Project name:** `corebox` (hoặc tên tùy thích, đường link sẽ là `https://corebox.pages.dev`).
   - **Production branch:** `main`
   - **Framework preset:** `None`
   - **Build command:** `py build_pages.py` (hoặc để trống vì thư mục `public/` đã được build sẵn).
   - **Build output directory:** `public`
   - Bấm **Save and Deploy**.
4. **Hoàn tất:** Sau khoảng 30 giây, website của bạn sẽ hoạt động chính thức trên toàn cầu tại địa chỉ:
   ```
   https://corebox.pages.dev
   ```

### Xem Trước Bản Cloudflare Pages Cục Bộ:
Nhấp đúp chuột vào file:
- [`preview_pages_local.bat`](file:///e:/OneDrive%20-%20Bac%20Giang/Desktop/3.%20BQLDA/10.%20Project%20Corebox/preview_pages_local.bat)  
Trình duyệt sẽ tự động mở `http://localhost:8080` để bạn kiểm tra giao diện và tính năng của bản build Cloudflare Pages.

---

### Cách 1: Chạy Cục Bộ (Local)
Nhấp đúp chuột vào tệp `run_local.bat` hoặc chạy lệnh sau trong PowerShell / CMD:
```powershell
py -m streamlit run app.py
```
Truy cập: `http://localhost:8501`

### Cách 2: Chia Sẻ Trực Tuyến Miễn Phí Qua Cloudflare Tunnel
Nhấp đúp chuột vào tệp `run_tunnel.bat`. Tệp sẽ tự động:
1. Khởi động ứng dụng COREBOX Web App.
2. Kết nối tới Cloudflare Tunnel thông qua `cloudflared.exe`.
3. Cung cấp một đường link HTTPS công khai miễn phí dạng:
   ```
   https://<random-id>.trycloudflare.com
   ```
Bạn có thể copy đường link này gửi cho đối tác hoặc đồng nghiệp để họ truy cập ngay từ bất cứ đâu trên điện thoại hoặc máy tính mà không cần cài đặt gì thêm!

---

## ☁️ Cấu Hình Cloudflare D1 & Cloudflare Access

### 1. Kết nối Cơ sở dữ liệu Cloudflare D1 (Tùy chọn)
Mặc định hệ thống dùng SQLite cục bộ (`data/corebox.db`). Khi muốn chuyển sang Cloudflare D1 trên đám mây:
1. Đăng nhập Cloudflare Dashboard ➔ **Workers & Pages** ➔ **D1 SQL Database** ➔ Tạo database mới tên `corebox_db`.
2. Tạo API Token có quyền truy cập D1.
3. Đổi tên file `.env.example` thành `.env` và điền:
   ```env
   CLOUDFLARE_ACCOUNT_ID=ma_tai_khoan_cloudflare_cua_ban
   CLOUDFLARE_D1_DATABASE_ID=ma_database_d1_cua_ban
   CLOUDFLARE_API_TOKEN=token_api_cua_ban
   ```

### 2. Cấu hình Cổng ngoài Cloudflare Access (Zero Trust)
1. Trong Cloudflare Dashboard, vào **Zero Trust** ➔ **Access** ➔ **Applications**.
2. Thêm ứng dụng Self-Hosted trỏ tới domain của bạn hoặc Cloudflare Tunnel.
3. Trong mục **Identity Providers**, thêm **Google Login**.
4. Trong mục **Policies**:
   - Chọn Action: `Allow`
   - Rule: `Emails ending in @gmail.com` hoặc `Everyone`.
   - Cổng ngoài sẽ cho phép tài khoản Google đăng nhập thành công vào ứng dụng; khi vào ứng dụng, hệ thống Corebox sẽ chặn lại ở màn hình chờ duyệt nếu email đó chưa được Admin `happyclone96@gmail.com` phê duyệt!

---

## 📂 Dữ Liệu Mẫu Để Kiểm Thử (Sample Data)

Thư mục `sample_data/` đã được tạo sẵn 3 tệp mẫu thực tế:
1. `sample_data/danh_muc_dinh_muc_mau.xlsx`: Danh mục định mức mẫu chứa các mã ngắn `AB.123`, `AF.1234`... để thử nghiệm tính năng trích xuất và tự động đệm 0 thành `AB.12300`, `AF.12340`.
2. `sample_data/danh_muc_dinh_muc_mau.docx`: Tệp Word mẫu chứa văn bản mở đầu và bảng mã định mức.
3. `sample_data/du_toan_kiem_tra_DGTH.xlsx`: Tệp dự toán có chứa sheet `ĐGTH` với 3 Hạng mục công trình lặp lại STT từ 1 và chứa cả mã đúng lẫn mã sai lệch để thử nghiệm chức năng kiểm tra mã.

---

## 🐙 Đẩy Lên GitHub

Để đưa mã nguồn lên GitHub của bạn:
```powershell
git add .
git commit -m "Khoi tao he thong COREBOX hoan chinh"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/corebox.git
git push -u origin main
```
