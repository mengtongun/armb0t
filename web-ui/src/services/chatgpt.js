import { Configuration, OpenAIApi } from "openai";

export const configuration = new Configuration({
  apiKey: import.meta.env.VITE_OPENAI_API_KEY,
});
export const openai = new OpenAIApi(configuration);

export const completion = async (prompt) =>
  await openai.createCompletion({
    model: "text-davinci-003",
    prompt,
  });

export const aiResponseBool = async (prompt) => {
  const response = await openai.createCompletion({
    prompt,
    model: "text-davinci-003",
    temperature: 0,
    max_tokens: 60,
    top_p: 1,
    frequency_penalty: 0.5,
    presence_penalty: 0,
  });
  return response.data.choices[0].text === "True";
};

export const aiResponse = async (prompt) => {
  const response = await openai.createCompletion({
    prompt,
    model: "text-davinci-003",
    temperature: 0,
    max_tokens: 60,
    top_p: 1,
    frequency_penalty: 0.5,
    presence_penalty: 0,
  });
  return response.data.choices[0].text;
};
export const decideQuestions = async (prompt) => {
  return aiResponse(
    `Decide whether a User\'s is asking to start engine. then reply with engine:true
    else if a User\'s ask the bot to choose or pick or grab color in this "blue,red,green". then reply with this format color:{color} only in lowercase and if the color in not in the list then generate prompt again with clearly explain that color is not detected by camera ai.
    else if a User\'s is asking to move arm. then reply with this format arm:true
    else if a User\'s is asking the robot arm to move to base. then reply with base:true
    else generate good explain the user to prompt again.
    \n\nUser: "${prompt}"\n\n`
  );
};

export const startingEngineResponse = async () => {
  return aiResponse(
    'if bot said engine:true then generate good explain to them that the engine is starting\n\nUser: " engine:true "\n\n'
  );
};

export const movingToBaseResponse = async () => {
  return aiResponse(
    "Generate good explain for the context that the robot arm is moving to base."
  );
};

export const pickingRedColorResponse = async (color) => {
  return aiResponse(
    `Generate good explain for the context that the robot arm is picking ${color} color.`
  );
};
