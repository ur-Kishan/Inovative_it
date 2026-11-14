4-BIT ALU DESIGN AND SIMULATION

Student: Kishan Pandey
Roll Number: 202610101070004
Course: M.Tech (CS)
Subject: Digital Electronics & Computer Organization
Subject Code: PCS1001
Submitted to: Prabhat Srivastava, Faculty, Digital Electronics & Computer Organization (PCS1001)
University: Shri Ramswaroop Memorial University

FILES
- 4-Bit_ALU_Design_and_Simulation.pptx : 22-slide presentation (light ivory / burnt-orange engineering theme, distinct from the 8-bit processor deck)
- 4-Bit_ALU_Project_Report.docx        : editable project report
- 4-Bit_ALU_Project_Report.pdf         : PDF report
- alu_4bit_sim.py                     : runnable reference simulator

OPERATIONS
000 ADD     R=(A+B) mod 16
001 SUB     R=(A-B) mod 16; C=1 means no borrow
010 AND     R=A AND B
011 OR      R=A OR B
100 XOR     R=A XOR B
101 NOT A   R=NOT A (four bits)
110 INC A   R=(A+1) mod 16
111 PASS B  R=B

FLAGS
Z=1 when result is zero. N=result bit 3. For ADD/INC, C is carry-out.
For SUB, C=1 means no borrow. V is signed two's-complement overflow for
ADD/SUB/INC and 0 for logic/PASS operations.

RUN
    python alu_4bit_sim.py

The simulator exhaustively checks 16 x 16 x 8 = 2,048 legal combinations.
Expected result: PASS - 2048/2048 exhaustive opcode/input checks.

SUBMISSION CHECKLIST
1. Create a GitHub repository and upload the report, presentation, source, and README.
2. Replace [INSERT REPOSITORY URL BEFORE SUBMISSION] in both documents with the real URL.
3. Verify the university/department details and sign/date the declaration if required.
4. Submit the PPT and report to Prabhat Srivastava through the required Google Classroom workflow.
