import json
from openai import OpenAI
import os
import sqlite3
from time import time

print("Starting script")
fdir = os.path.dirname(__file__)
def getPath(fname):
  return os.path.join(fdir, fname)

# SQLITE
sqliteDBPath = getPath("aidb.sqlite")
createSchemaPath = getPath("../db/sqlite/table_schema.sql")
insertDataPath = getPath("../db/sqlite/data_population.sql")

# Erase previous db
if os.path.exists(sqliteDBPath):
  os.remove(sqliteDBPath)

# Create new SQLite DB
sqliteConn = sqlite3.connect(sqliteDBPath)
sqliteCursor = sqliteConn.cursor()
with (open(createSchemaPath) as createSchemaFile, open(insertDataPath) as insertDataFile):
  createSchemaScript = createSchemaFile.read()
  insertDataScript = insertDataFile.read()
sqliteCursor.executescript(createSchemaScript) # create tables
sqliteCursor.executescript(insertDataScript) # insert data
print("Database created and populated")

def runSQL(query):
  return sqliteCursor.execute(query).fetchall()

# OPENAI
configPath = getPath("../config.json")
with open(configPath) as configFile:
  config = json.load(configFile)

openAIClient = OpenAI(api_key = config["open-ai-key"])
openAIClient.models.list() # check the key is valid

def getChatGPTResponse(content):
  stream = openAIClient.chat.completions.create(
    model = "gpt-4o",
    messages = [{"role": "user", "content": content}],
    stream = True
  )
  responseList = []
  for chunk in stream:
    if chunk.choices[0].delta.content is not None:
      responseList.append(chunk.choices[0].delta.content)
  return "".join(responseList)

# Strategies
exampleQuestion = "What has Yoshi's lowest ranking been?"
exampleAnswer = "SELECT MAX(`rank`) AS LowestRank FROM `Character` LEFT JOIN TierEntry ON `Character`.id = TierEntry.character_id GROUP BY `Character`.name HAVING `Character`.name = 'Yoshi';"
commonSQLOnlyRequest = " Give me a sqlite SELECT statment that answers the question. Only respond with sqlite syntax. If there is an error do not explain it! Remember to quote reserved keywords like Character and rank with backticks."
strategies = {
  "zero_shot": createSchemaScript + commonSQLOnlyRequest,
  "single_domain_double_shot": f"{createSchemaScript} {exampleQuestion} {exampleAnswer} + {commonSQLOnlyRequest}"
}

questions = [
  "Who is currently the highest-ranked character in the game?",
  "What players have been rank 1?",
  "How many players have been rank 1 while one of their mains was also rank 1?",
  "What has Yoshi's lowest ranking been?",
  "What has Yoshi's highest ranking been?",
  "What character has the biggest difference in lowest and highest ranking?",
  "How many players have ever been in the top 100?",
  "What are the top 5 characters right now?",
  "What is currently the highest-ranking character that has ever received an F or G ranking?",
  "What was the most popular character pick among top 100 players in 2022?",
  "What were Armada's mains in 2015?"
]

def santizeForJustSQL(value):
  gptStartSQLMarker = "```sqlite"
  gptAlternateStartSQLMarker = "```sql"
  gptEndSQLMarker = "```"
  if gptStartSQLMarker in value:
    value = value.split(gptStartSQLMarker)[1]
  elif gptAlternateStartSQLMarker in value:
    value = value.split(gptAlternateStartSQLMarker)[1]
  if gptEndSQLMarker in value:
    value = value.split(gptEndSQLMarker)[0]
  return value

for strategy in strategies:
  responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
  questionResults = []
  print("=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====")
  print(f'Running strategy: {strategy}')
  for question in questions:
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Question:")
    print(question)
    error = "None"

    try:
      sqlSyntaxResponse = santizeForJustSQL(getChatGPTResponse(strategies[strategy] + " " + question))
      print("SQL Syntax Response:")
      print(sqlSyntaxResponse)
      queryRawResponse = str(runSQL(sqlSyntaxResponse))
      print("Query Raw Response:")
      print(queryRawResponse)
      friendlyResultsPrompt = f"I asked a question: \"{question}\" and I queried this database {createSchemaScript} with this query {sqlSyntaxResponse}. The query returned the results data: \"{queryRawResponse}\". Could you concisely answer my question using the results data?"
      friendlyResponse = getChatGPTResponse(friendlyResultsPrompt)
      print("Friendly Response:")
      print(friendlyResponse)
    except Exception as err:
      error = str(err)
      print(f"\033[31m{err}\033[0m")
    questionResults.append({
      "question": question,
      "sql": sqlSyntaxResponse,
      "queryRawResponse": queryRawResponse,
      "friendlyResponse": friendlyResponse,
      "error": error
    })
  responses["questionResults"] = questionResults

  # Write responses to file
  # TODO: Consider outputting it some other way, maybe in addition
  with open(getPath(f"../responses/response_{strategy}_{time()}.json"), "w") as outFile:
    json.dump(responses, outFile, indent = 2)

sqliteCursor.close()
sqliteConn.close()
print("Finished script")