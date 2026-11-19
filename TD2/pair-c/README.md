
TD2 — Pair C: AI Model Routing Policy and Simulator
Project Objective
Our task was to design and implement a routing policy for selecting AI models based on their TD1 accuracy, cost, availability, and request risk.

We used the results from 20 TD1 questions to define model-selection rules and adapted the professor's Python simulator to test these decisions.

1. Routing Policy and Analysis
Role: Routing policy design, TD1 accuracy analysis, and final report.

Work completed:

Analyzed the accuracy of five AI models across eight question families.
Selected suitable models based on TD1 results and portfolio costs.
Defined verification rules for internal dashboards, customer-facing figures, and payout amounts.
Established fallback rules for unavailable models.
Analyzed the seven routing scenarios before and after adaptation.
Explained when the system should run, defer, or abstain.
Prepared the final TD2 report.
2. Routing Simulator Implementation and Testing
Role: Python routing simulator implementation and validation.

Work completed:

Adapted the professor's original atelier-routage.py simulator using the Pair C routing policy.
Replaced the fictional resources with GPT-20B, GPT-120B, and Qwen.
Integrated TD1 accuracy results for all eight question families: F1, F2, F2b, F3, F1+F3, F1+F2, F2+F3, and F1+F2+F3.
Modified the choose() function to select eligible models based on accuracy, availability, and request constraints.
Implemented fallback, quota waiting, and abstention logic.
Added verification requirements for internal, customer-facing, and payout requests.
Executed and compared the seven original and modified routing scenarios.
Tested fallback behavior and customer-facing verification requirements.
Tested model selection for all eight families, with 8/8 tests passed.
3. Routing Decisions
The adapted simulator supports three possible decisions:

Run: Select an eligible and available model.
Defer: Wait for a free model's quota to reset when the deadline allows it.
Abstain: Do not proceed when no eligible model is available.
For example, GPT-20B is selected for F1 because it achieved 6/6 in TD1, while GPT-120B is selected for F2 because it achieved 4/4.

4. Project Files
File	Description
TD2/routing-policy.md	Routing policy and TD1 accuracy analysis
TD2/pair-c/atelier-routage.py	Adapted Python routing simulator
TD2/pair-c/atelier-routage-original.py	Original simulator backup
TD2/pair-c/results-before.txt	Results before adaptation
TD2/pair-c/results-after.txt	Results after adaptation
TD2/pair-c/deferrable-after.txt	Isolated deferrable scenario
TD2/reports/td2.md	Final group report
5. How to Run the Simulator
From the root of the NextGen repository, execute:

python TD2/pair-c/atelier-routage.py
To run only the deferrable scenario:

python TD2/pair-c/atelier-routage.py --scenario deferrable
6. Testing and Validation
The adapted simulator was tested using seven scenarios: simple, complex, deferrable, urgent, budget exhausted, high impact, and unknown capability.

Additional tests confirmed the fallback behavior and the customer-facing verification requirement.

All eight family-selection tests passed, confirming that the simulator selects the expected first-choice model for each family under the tested availability conditions.

7. Limitations
Routing decisions are based on only 20 TD1 questions, so the observed accuracy does not guarantee future model performance.
Model availability and quota information are simulated.
The simulator specifies the required verification methods but does not execute them.
No real AI API calls are made.