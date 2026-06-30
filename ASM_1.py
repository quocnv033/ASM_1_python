import os
import pandas as pd
import re 

# khai báo tệp và folder lưu file
opened_file_name  = None
INPUT_FOLDER = "text_file"
OUTPUT_FOLDER = "expected_output"


#xóa màn hình để tránh chồng chất output
def clear_screen():
    os.system("cls")      # Windows


# Hàm in báo cáo cho các câu hỏi bị bỏ qua hoặc trả lời sai nhiều nhất
def report(title, counts, total_students):
    # Tìm số lượng lớn nhất trong danh sách (số lần bị bỏ qua/sai nhiều nhất)
    max_count = max(counts)
    if max_count == 0:  # Nếu không có câu nào bị bỏ qua/sai thì thoát
        return
    print(f"\n{title}")

    # Duyệt qua từng câu hỏi
    for i, c in enumerate(counts):
        if c == max_count:  # Chỉ in những câu có số lượng bằng max_count
            
            # In số thứ tự câu hỏi, số học sinh, và tỉ lệ %
            print(f"Q{i+1} - {c} students - {c/total_students:.2%}")


# đọc file và kiểm file có tồn tại hay không 
def option_1_open_file():
    global opened_file_name

    #change 
    while True:
        file_name = input("Enter a class file to grade: ")
        
        # vì file lưu trong folder riêng, ghép thành đường dẫn đầy đủ
        file_path = os.path.join(INPUT_FOLDER, file_name)

        try:
            pd.read_table(file_path, header=None)
            opened_file_name = file_path

            print("\nFile opened successfully!")
            input("\nPress Enter to continue...")
            clear_screen()
            return

        except FileNotFoundError:
            clear_screen()
            show_menu()
            print("\nFile cannot be found. Please try again.\n")


# kiểm tra các dòng hợp lệ trong file
def option_2_validate_file():

    if opened_file_name is None:
        print("Please open a file first using Option 1.")
        input("\nPress Enter to continue...")
        clear_screen()
        return

    df = pd.read_table(opened_file_name, header=None, names=["line"], dtype=str)

    total_lines, invalid_lines = 0, 0
    print("**** Analyzing... ****\n")

    for line in df["line"]:
        total_lines += 1

        #chuyển sang chuỗi và xóa khoảng trắng thừa
        line = str(line).strip()

        # tách dữ liệu trong một dòng thành danh sách các giá trị,
        # dựa trên dấu phẩy , làm ký tự phân cách.
        values = line.split(",")

        # Các điều kiện kiểm tra
        errors = []
        if len(values) != 26:
            errors.append("does not contain exactly 26 values")
        elif not re.fullmatch(r"N\d{8}", values[0]):
            errors.append("invalid student ID")
        elif "" in values[1:]:
            errors.append("contains blank answers")

        if errors:
            print("Invalid line of data:", ", ".join(errors))
            print(line)
            invalid_lines += 1

    if invalid_lines == 0:
        print("No errors found!")

    print("\n**** REPORT ****")
    print(f"Total lines of data: {total_lines}")
    print(f"Total invalid lines of data: {invalid_lines}")

    input("\nPress Enter to continue...")
    clear_screen()


# hàm thực thi option 3
def option_3_grade_exams():
    # Kiểm tra người dùng đã mở file chưa
    if opened_file_name is None:
        print("Please open a file first using Option 1.")
        input("\nPress Enter to continue...")
        clear_screen()
        return

    # Đáp án chuẩn cho 25 câu hỏi
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(",")

    # Đọc dữ liệu từ file
    df = pd.read_table(opened_file_name, header=None, names=["line"], dtype=str)

    # Danh sách điểm của học sinh
    scores = []

    # Đếm số lần bỏ qua và trả lời sai cho từng câu hỏi
    skipped, wrong = [0]*25, [0]*25

    # Duyệt từng dòng dữ liệu trong file
    for line in df["line"]:
        values = str(line).strip().split(",")
        # Kiểm tra dòng hợp lệ: đủ 26 giá trị và ID đúng định dạng
        if len(values) != 26 or not re.fullmatch(r"N\d{8}", values[0]):
            continue

        student_answers, score = values[1:], 0
        # Chấm từng câu hỏi
        for i, ans in enumerate(student_answers):
            if ans == "":  # Bỏ qua
                skipped[i] += 1
            elif ans == answer_key[i]:  # Trả lời đúng
                score += 4
            else:  # Trả lời sai
                score -= 1
                wrong[i] += 1
        scores.append(score)  # Lưu điểm học sinh

    # Nếu không có dữ liệu hợp lệ
    if not scores:
        print("No valid student records.")
        input("\nPress Enter to continue...")
        clear_screen()
        return

    # Chuyển sang Series để tính toán thống kê dễ dàng
    scores = pd.Series(scores)

    # In báo cáo thống kê
    print("\n\n**** GRADING REPORT ****\n")
    print("3.1 High scores (>80):", (scores > 80).sum())
    print("3.2 Mean score:", round(scores.mean(), 2))
    print("3.3 Highest score:", scores.max())
    print("3.4 Lowest score:", scores.min())
    print("3.5 Range:", scores.max() - scores.min())
    print("3.6 Median:", scores.median())

    # Gọi hàm report cho phần 3.7 và 3.8
    report("3.7 Most skipped questions:", skipped, len(scores))
    report("3.8 Most incorrect questions:", wrong, len(scores))

    input("\nPress Enter to continue...")
    clear_screen()


# ghi ID và điểm vào file text
def option_4_export_grades():
    # Kiểm tra đã mở file chưa
    if opened_file_name is None:
        print("Please open a file first using Option 1.")
        input("\nPress Enter to continue...")
        clear_screen()
        return

    # Đáp án chuẩn
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(",")
    df = pd.read_table(opened_file_name, header=None, names=["line"], dtype=str)

    results = []
    for line in df["line"]:
        values = str(line).strip().split(",")

        # Kiểm tra hợp lệ: đủ 26 giá trị và ID đúng định dạng
        if len(values) != 26 or not re.fullmatch(r"N\d{8}", values[0]):
            continue

        student_id, answers = values[0], values[1:]

        # Tính điểm bằng list comprehension
        score = sum(
            4 if ans == key else -1 if ans != "" else 0
            for ans, key in zip(answers, answer_key)
        )
        results.append([student_id, score])

    if not results:
        print("No valid student records.")
        input("\nPress Enter to continue...")
        clear_screen()
        return

    # Lấy tên file gốc (class1.txt, class2.txt,...)
    base_name = os.path.splitext(os.path.basename(opened_file_name))[0]

    # Tạo đường dẫn file kết quả
    output_file = os.path.join(OUTPUT_FOLDER, base_name + "_grades.txt")

    # Ghi DataFrame ra file
    pd.DataFrame(results).to_csv(output_file, index=False, header=False)

    print("\nGrades have been saved to:")
    print(output_file)

    input("\nPress Enter to continue...")
    clear_screen()


def show_menu():
    print("\n===== MENU =====")
    print("1. Open a class file")
    print("2. Analysis file")
    print("3. Grade exams")
    print("4. Export grade to file")
    print("5. Exit")



while True:
    
    show_menu()
    
    choice = input("Choose an option (1-5): ")

    if choice == "1":
        option_1_open_file()

    elif choice == "2":
        option_2_validate_file()

    elif choice == "3":
        option_3_grade_exams()

    elif choice == "4":
       option_4_export_grades()

    elif choice == "5":
        print("Program ended.")
        break

    else:
        print("Invalid choice. Please choose from 1 to 5.")