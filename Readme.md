Giới thiệu dự án Kinh Thánh Mỗi Ngày:

Thời gian vừa rồi mình có tìm hiểu một chút về chatbot và muốn bắt tay thực hiện một dự án chatbot đơn giản nhất có thể, nhưng cũng cố gắng làm sao có đầy đủ các thành phần để ít ra cũng hữu ích một chút.

Mục đích của project này là xây dựng một cái chatbot có khả năng hỏi xem user đang cảm thấy thế nào, và đưa ra một câu Kinh Thánh phù hợp với cảm xúc đó.

Mô hình của chatbot gồm 3 phần chính:

- Conversation flow: Mô hình cuộc trò chuyện sẽ được quyết định ở đây. Cái này mình sử dụng nền tảng Botstar (made in Vietnam luôn). Tất cả các thứ liên quan đến cuộc hội thoại được xử lý bởi phần này hết. Đến đoạn user chọn được một chủ đề, chatbot sẽ gửi POST request sang phần thứ 2 để nhận về nội dung câu gốc.
- Verses controller: Nhiệm vụ của anh này là nhận yêu cầu từ chatbot và gửi về một câu gốc theo yêu cầu. Cái này mình viết vài file php đơn giản để get câu Kinh Thánh từ file JSON đã tạo sẵn.
- Data maker: Phần này hoàn toàn offline, có nhiệm vụ thu thập các câu Kinh Thánh theo chủ đề, rồi lưu vào file JSON. Sau đó mình upload file này lên server để verses controller xài. Code viết trên python.

##todo
- Refactor lại source code, bỏ những file từ phiên bản cũ.
- Sync luôn phần php vào đây.