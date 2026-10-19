\# Olist SQL Assistant



Ask questions about an e-commerce database in plain English. The app writes the SQL, runs it, and shows a table, a chart, and the query it used.



\*\*Live demo:\*\* https://olist-sql-assistant.streamlit.app/

(Free hosting, so it may take about 30 seconds to wake up. Each visitor gets 10 questions.)



\## Why I built this



Most people at a company can't write SQL, and AI can write it but sometimes invents things. So the real question is how much you can trust AI-generated SQL, and what makes it more reliable. I built the tool, then measured its accuracy against hand-written answers.



\## How it works



1\. The user's question, the exact table and column names (read from the database), and a plain-English data dictionary go to a Gemini model, which writes one SQL query.

2\. A safety check allows only SELECT queries and blocks words like DROP, DELETE and UPDATE.

3\. The query runs on a read-only DuckDB connection, with results capped at 200 rows.

4\. If the query fails, the error message goes back to the model once so it can correct itself.

5\. Streamlit shows the table, a bar chart, the SQL used, and thumbs up/down buttons.



\## Data



Brazilian E-Commerce Public Dataset by Olist (Kaggle): about 100,000 orders from 2016 to 2018 across 9 related tables (orders, customers, items, payments, reviews, products, sellers, and more).



\## Evaluation



I wrote 20 test questions (4 easy, 8 medium, 8 hard) with correct SQL. The script asks the assistant each question, runs both queries, and compares the \*\*result sets\*\* (sorted, numbers rounded to 2 decimals), not the SQL text, because different queries can both be correct.



I ran the same 20 questions under three setups:



| Setup | Overall | Easy | Medium | Hard |

|---|---|---|---|---|

| 1. No context (model guesses) | 75% (15/20) | 25% | 100% | 75% |

| 2. Exact schema only | 100% (20/20) | 100% | 100% | 100% |

| 3. Exact schema + data dictionary | 95% (19/20) | 100% | 100% | 88% |



\*\*What I found:\*\* giving the model the exact schema raised accuracy from 75% to 100%. Adding the data dictionary on top did not measurably help (the 100% vs 95% gap is one question out of 20, within normal run-to-run variation).



\*\*The 5 failures with no context:\*\*

\- 3 invented names: a table called `olist\_order\_reviews\_dataset`, a column `item\_price` (real name: `price`), and a column `category` that doesn't exist.

\- 2 wrong-meaning errors: counting `customer\_id` (changes every order) instead of `customer\_unique\_id` for "unique customers", and defining "delivered" by a date column instead of `order\_status`.



Schema grounding fixes the invented names. The wrong-meaning errors are the kind a data dictionary should help with, but my test set had too few ambiguous questions to show it.



\## Business insights (found with SQL on the same data)



1\. \*\*Late deliveries hurt reviews.\*\* 7.99% of delivered orders (7,661) arrived late. Late orders averaged 2.57 out of 5, against 4.29 for on-time orders. Recommended action: flag at-risk orders early and set more realistic delivery estimates. This shows a link, not proof of cause.

2\. \*\*Some states are much worse at on-time delivery.\*\* Maranhao (MA) is late on 19.67% of orders, Ceara (CE) on 15.32%, Bahia (BA) on 14.04%, against about 8% overall. Rio de Janeiro (RJ) is late on 13.47% of 12,350 orders, so it affects the most customers. Recommended action: investigate carriers and routes in these states. Caveat: the estimated date is set by the platform, so lateness may reflect optimistic estimates, not slow shipping.

3\. \*\*Revenue is concentrated and customers rarely return.\*\* Sao Paulo alone brings in 38.28% of item revenue, and the top 3 states about 63%. Only 3.12% of customers (2,997 of 96,096) ordered more than once. Recommended action: protect delivery quality in the top states and test offers that bring first-time buyers back.



\## Limitations



\- Only 20 test questions, each setup run once. The model can answer differently on repeat runs, so small gaps are not meaningful.

\- I wrote both the questions and the correct answers, and most questions are clearly worded. Real users ask vaguer questions.

\- One hard question failed in the full setup (highest-revenue month). The assistant grouped revenue by delivery date, while my answer key used purchase date. My question didn't say which date to use, so this was an ambiguous test question, not a clear model error. I kept the 95% result as measured instead of rewording the question and re-running.- The model name is an alias (`gemini-flash-lite-latest`), so results may change when the underlying model changes.

\- The business insights are correlations from one dataset covering 2016 to 2018.

\- The demo runs on a free API tier with usage limits.



\## Next steps



Add 30 to 40 harder and ambiguous questions, repeat each setup 3 times, add example questions to the prompt, and make the tool say "I can't answer that" when the data doesn't contain the answer.



\## Run it yourself



1\. Install Python 3.12 or newer.

2\. Install packages: pip install -r requirements.txt

3\. Set your Gemini API key: set GEMINI\_API\_KEY=your-key (Windows)

4\. Start the app: python -m streamlit run app.py

5\. Run the evaluation: python eval.py (use set MODE=none, schema\_only or full to switch setups)



\## Files



\- app.py: the Streamlit chat interface with usage limits

\- ask.py: question to SQL, safety checks, retry

\- eval.py and tests\_hard.py: the evaluation

\- compare.py: builds the accuracy table

\- insights.py: SQL behind the business insights

\- data\_dictionary.md: plain-English description of the tables

\- olist.duckdb: the database



Built by Nayanika S. Tools: Python, DuckDB, Streamlit, Gemini API, pandas.

