# Báo Cáo

## Kết quả sau khi chạy `benchmark.py` và phân tích kết quả `benchmark_result.json`

| Metric | Kết quả |
|---|---|
| Thời gian load data | 2.358 s |
| Thời gian training | 2.259 s |
| Best iteration | 1 |
| AUC-ROC | 0.9381 |
| Accuracy | 0.9991 |
| F1-Score | 0.7644 |
| Precision | 0.6772 |
| Recall | 0.8776 |
| Inference latency (1 row) | 1.164 ms/row (mean of 200 runs) |
| Inference throughput (1000 rows) | ~708,734 rows/s (1000 rows in 1.41 ms, median of 10 runs) |

> Note: `best_iteration = 1` is anomalous. After re-running with early stopping on validation AUC (patience 50, `first_metric_only=True`), best_iteration and all quality metrics are unchanged, so the cause is not logloss-based early stopping; root cause is still under investigation.

## Giải thích: AUC dùng xác suất, throughput tính bằng dòng/giây

**Vì sao AUC-ROC dùng xác suất (`predict_proba`) chứ không dùng nhãn dự đoán?**
- AUC-ROC đo khả năng *xếp hạng* của model: xác suất một giao dịch gian lận được chấm điểm cao hơn một giao dịch bình thường ngẫu nhiên. Nó được tính bằng cách quét mọi ngưỡng quyết định có thể, nên cần điểm số liên tục (xác suất `P(Class=1)`).
- Nhãn dự đoán (0/1) là kết quả sau khi đã cắt ngưỡng cố định (ở đây 0.5). Nếu đưa nhãn vào, đường ROC chỉ còn một điểm thật sự, mất thông tin thứ hạng và AUC không còn phản ánh chất lượng model.
- Ngược lại, Accuracy/F1/Precision/Recall là các metric *tại một ngưỡng cụ thể*, nên dùng nhãn dự đoán. Với dữ liệu gian lận rất mất cân bằng (492/284,807 dòng ≈ 0.17%), AUC giúp đánh giá model độc lập với việc chọn ngưỡng, còn Accuracy dễ gây ngộ nhận (đoán toàn "không gian lận" cũng đạt ~99.8%).

**Vì sao throughput có đơn vị dòng/giây?**
- Throughput là *lượng công việc hoàn thành trên một đơn vị thời gian*; công việc ở đây là số dòng dữ liệu được dự đoán, nên đơn vị là dòng/giây (rows/s). Công thức: `throughput = 1000 / thời_gian_giây`, với thời gian là của cả batch 1.000 dòng (≈ 1.41 ms, lấy median 10 lần) → 1000 / 0.00141 ≈ 708,734 rows/s.
- Khác với latency (thời gian cho *1 dòng*, đơn vị ms/dòng), throughput đo khả năng xử lý theo batch. Batch lớn tận dụng vector hóa và chia nhỏ chi phí gọi hàm cố định, nên throughput cao hơn nhiều so với `1 / latency` của dự đoán từng dòng (1 / 1.164 ms ≈ 859 rows/s).

## Báo cáo ngắn: nhận xét kết quả trên CPU (`t3.medium`, 2 vCPU / 4 GB RAM)

1. **Training time:** LightGBM huấn luyện trên 170,883 dòng chỉ mất ~2.26 s trên CPU 2 vCPU, nhanh hơn thời gian load CSV (~2.36 s). Bài toán dạng bảng với gradient boosting không cần GPU.
2. **AUC-ROC:** đạt 0.9381, Recall 0.8776 (bắt được ~88% giao dịch gian lận) nhưng Precision chỉ 0.6772, F1 0.7644. Accuracy 0.9991 cao do dữ liệu mất cân bằng (~0.17% gian lận) nên không phản ánh đúng chất lượng model.
3. **Điểm bất thường:** `best_iteration = 1`, tức validation AUC không cải thiện sau cây đầu tiên, nên model gần như chưa được boosting. Đổi early stopping sang AUC (patience 50) không thay đổi kết quả, nguyên nhân gốc chưa xác định. Vì vậy AUC 0.938 có thể thấp hơn mức model đạt được nếu tinh chỉnh.
4. **Inference speed:** dự đoán 1 dòng mất ~1.16 ms (~859 dòng/s nếu gọi từng dòng), còn dự đoán theo batch 1,000 dòng đạt ~708,734 dòng/s (~1.41 ms/batch). Dự đoán theo batch nhanh hơn rất nhiều nhờ chia nhỏ chi phí gọi hàm cố định.
5. **Kết luận:** CPU nhỏ đáp ứng tốt cả training và inference cho bài toán này (chi phí ~$0.10/giờ cho cả hạ tầng), nhưng cần điều tra `best_iteration = 1` trước khi coi chất lượng model là đáng tin.