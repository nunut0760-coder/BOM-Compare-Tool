## BOM Compare Tool - User Guide



## Introduction

**BOM Compare Tool** is a lightweight desktop application designed to compare two BOM (Bill of Materials) text files quickly and accurately. It automatically identifies differences in component information and generates an Excel report for easy review.



## Main Features

* Compare two BOM text files.
* Detect Part Number differences.
* Detect Component Value/Description differences.
* Identify duplicate RefDes entries.
* Support customizable Ignore Words to filter unnecessary descriptions.
* Export comparison results to an Excel report.
* Built-in comparison log for monitoring the processing status.



## How to Use



##### Step 1. Select BOM Files

* Click **Browse** next to **File1** and select the first BOM file.
* Click **Browse** next to **File2** and select the second BOM file.



##### Step 2. Configure Ignore Words (Optional)

The **Ignore Words** list allows users to remove specific keywords from component descriptions before comparison.

* Check or uncheck keywords to enable or disable them.
* Add new keywords if required.
* Delete unnecessary keywords from the list.



##### Step 3. Start Comparison

Click **Compare BOM** to begin the comparison.

The program will:

* Parse both BOM files.
* Compare all RefDes entries.
* Detect Part Number and Value differences.
* Generate an Excel comparison report.



##### Step 4. Review Results

After the comparison is complete, an Excel report will be generated automatically.

The report includes:

* **Differences** – All detected BOM differences.
* **Duplicate\_File1** – Duplicate RefDes found in File1.
* **Duplicate\_File2** – Duplicate RefDes found in File2.

The processing log displayed at the bottom of the application shows the comparison progress and completion status.



## Notes

* Input files should be exported as plain **.txt** files.
* Ignore Words affect only the comparison of component descriptions and do not modify the original BOM files.
* The generated Excel report is for reference only. Please review the results before applying any engineering changes.



\------------------------------------------------------------------------------

**Version:** 1.5.4

**Application:** BOM Compare Tool

**Author:** Liyan Shao

