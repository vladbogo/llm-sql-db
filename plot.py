from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
import matplotlib.pyplot as plt

# Replace with your OpenAI API key
openai_api_key = 'sk-<your-openai-api-key>'

# Database connection - replace with your database details
database_url = 'mysql://<username>:<password>@<host>:<port>/<database>'

# Initialize the database
db = SQLDatabase.from_uri(database_url)

# Initialize the language model
llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0, openai_api_key=openai_api_key)

# Create the SQL query chain
chain = create_sql_query_chain(llm, db)

# Get user's question
user_question = input("Enter your question: ")

# Generate the SQL query
response = chain.invoke({"question": user_question})
# Parse the SQL query from the response
try:
    sql_query = response.split("```sql")[1].split("```")[0].strip()
except IndexError:
    sql_query = None

if not sql_query:
    print("No SQL query generated.")
else:
    print("Generated SQL Query:", sql_query)

    # Ask for user confirmation
    confirmation = input("Do you want to execute this query? (yes/no): ")

    # Execute the query if confirmed
    if confirmation.lower() == 'yes':
        result = db.run(sql_query)
        # Extracting data for plotting
        query_result = eval(result)
        x_values = range(len(query_result))
        y_values = [item[-1] for item in query_result]

        # Plotting the data
        plt.figure(figsize=(10, 6))
        plt.scatter(x_values, y_values, marker='o')
        plt.title('Query Result Plot')
        plt.xlabel('X Values')
        plt.ylabel('Y Values')
        plt.grid(True)
        plt.savefig('plot.png')
    else:
        print("Query execution cancelled.")