# Day 16 Lab: Cloud AI infrastructure

## Overview

> https://vlearn.dev/course/k04-l34-p2-t2/reader?day=D04&part=codelab-3ff073e266314c1bbcdc532115e5d8c7-s01-doc

## CP0

1. Mở [repo bài lab](https://github.com/VinUni-AI20k/Day16-Track2-Assignment) trên GitHub.
2. Bấm Fork, chọn Owner là tài khoản GitHub cá nhân của bạn.
3. Giữ nguyên Repository name là Day16-Track2-Assignment, rồi bấm Create fork.
4. Kiểm tra repo vừa tạo có dạng <username>/Day16-Track2-Assignment, trong đó <username> là tên tài khoản GitHub của bạn. Đây là repo để lưu và nộp bài làm.

```bash
git clone git@github.com:<your-username-github>/Day16-Track2-Assignment.git
cd Day16-Track2-Assignment
touch benchmark.py benchmark_result.json REPORT.md

```

## CP1
> Tạo hạ tầng và SSH vào máy (AWS: Terraform + Bastion)

[Phần 1: Chuẩn bị tài khoản AWS và thiết lập IAM (Least-Privilege)](https://github.com/jaimesHub/Day16-Track2-Assignment/blob/main/README_aws.md#ph%E1%BA%A7n-1-chu%E1%BA%A9n-b%E1%BB%8B-t%C3%A0i-kho%E1%BA%A3n-aws-v%C3%A0-thi%E1%BA%BFt-l%E1%BA%ADp-iam-least-privilege) [x]

[Phần 2: Cài đặt và cấu hình môi trường Local](https://github.com/jaimesHub/Day16-Track2-Assignment/blob/main/README_aws.md#ph%E1%BA%A7n-2-c%C3%A0i-%C4%91%E1%BA%B7t-v%C3%A0-c%E1%BA%A5u-h%C3%ACnh-m%C3%B4i-tr%C6%B0%E1%BB%9Dng-local)

[Phần 3: Triển khai Hạ tầng với Terraform](https://github.com/jaimesHub/Day16-Track2-Assignment/blob/main/README_aws.md#ph%E1%BA%A7n-3-tri%E1%BB%83n-khai-h%E1%BA%A1-t%E1%BA%A7ng-v%E1%BB%9Bi-terraform)

```bash
terraform init
terraform validate
terraform plan
terraform apply
```

> benchmark time: 2:59,25

> create `ssh_config` file
> ssh -F ssh_config lab-cpu
> ProxyJump đi qua Bastion và dùng private key tại laptop để xác thực cả hai máy. Không cần copy private key lên Bastion. Hai lệnh SSH nối tiếp trong README cần thêm bước xác thực ở máy private; file config trên làm rõ bước đó.
> [Tham khảo đường kết nối Bastion của AWS.](https://repost.aws/knowledge-center/ec2-linux-private-subnet-bastion-host)


## CP2

[Phần 4: Kết nối và Huấn luyện mô hình LightGBM trên CPU Node](https://github.com/jaimesHub/Day16-Track2-Assignment/blob/main/README_aws.md#ph%E1%BA%A7n-4-k%E1%BA%BFt-n%E1%BB%91i-v%C3%A0-hu%E1%BA%A5n-luy%E1%BB%87n-m%C3%B4-h%C3%ACnh-lightgbm-tr%C3%AAn-cpu-node)

> NOTE: Nên follow theo [guide này](https://vlearn.dev/course/k04-l34-p2-t2/reader?day=D04&part=codelab-3ff073e266314c1bbcdc532115e5d8c7-s03-doc) để `SSH qua Bastion với key ở laptop` (Tức bước 4.1 ở README_aws.md)

[Phần 5: Kiểm tra Tài nguyên và Chi phí](https://github.com/jaimesHub/Day16-Track2-Assignment/blob/main/README_aws.md#ph%E1%BA%A7n-5-ki%E1%BB%83m-tra-t%C3%A0i-nguy%C3%AAn-v%C3%A0-chi-ph%C3%AD)

[Phần 6: Tiêu chí nộp bài (Deliverables)](https://github.com/jaimesHub/Day16-Track2-Assignment/blob/main/README_aws.md#ph%E1%BA%A7n-6-ti%C3%AAu-ch%C3%AD-n%E1%BB%99p-b%C3%A0i-deliverables)

[Phần 7: Dọn dẹp tài nguyên (CỰC KỲ QUAN TRỌNG)](https://github.com/jaimesHub/Day16-Track2-Assignment/blob/main/README_aws.md#ph%E1%BA%A7n-7-d%E1%BB%8Dn-d%E1%BA%B9p-t%C3%A0i-nguy%C3%AAn-c%E1%BB%B1c-k%E1%BB%B3-quan-tr%E1%BB%8Dng)

## CP3

## CP4

## CP5