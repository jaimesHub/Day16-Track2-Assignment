# FINAL REPORT

1. Tôi dùng AWS, us-east-1, Bastion Host (t3.micro) ở Public Subnet, Compute Node (t3.medium — 2 vCPU / 4 GB RAM) ở Private Subnet, source commit 2c9005f.
2. Dataset có 284,807 dòng (492 dòng gian lận), chia train/validation/test theo tỉ lệ 60/20/20 (170,883 / 56,962 / 56,962, stratified theo `Class`), seed 42.
3. Load dữ liệu mất 2.358 giây; training mất 2.259 giây; best iteration là 1 (bất thường: validation AUC không cải thiện sau cây đầu tiên; đổi early stopping sang AUC, patience 50 vẫn không đổi, nguyên nhân gốc chưa xác định).
4. AUC 0.9381, Accuracy 0.9991, F1 0.7644, Precision 0.6772, Recall 0.8776 trên tập test (ngưỡng 0.5; AUC tính từ xác suất, các metric còn lại từ nhãn dự đoán).
5. Latency 1 dòng 1.164 ms; throughput batch 1.000 dòng ~708,734 dòng/giây; cách đo: warm-up trước, latency là trung bình 200 lần dự đoán 1 dòng, throughput = 1000 / thời gian median của 10 lần dự đoán batch 1.000 dòng (~1.41 ms/batch).
6. CPU/RAM/Network tôi quan sát lúc 12:45 là [hình 1](./screenshots/aws-monitoring.png).
7. Billing tại 13:00 ghi nhận 0.03$, xem thêm tại [hình 1](./screenshots/billing-ec2.png), [hình 2](./screenshots/billing-elb-vpc.png).
8. Tôi đã tải kết quả và xóa tài nguyên lúc 13:30; bằng chứng dọn dẹp [đây](./screenshots/evidence-terraform-destroy.png).