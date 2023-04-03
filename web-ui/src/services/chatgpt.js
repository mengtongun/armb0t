import { Configuration, OpenAIApi } from "openai";

export const configuration = new Configuration({
  apiKey: "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",
});
export const openai = new OpenAIApi(configuration);

export const completion = async (prompt) =>
  await openai.createCompletion({
    model: "text-davinci-003",
    prompt,
  });

export const editModel = async (prompt) => {
  const { data } = await openai.createEdit({
    model: "text-davinci-edit-001",
    input: prompt,
    instruction:
      "Analyze the input whether the user want to chose any color then give then edit te response back to me as the color",
  });
  return data;
};

export const decideColor = async (prompt) => {
  const response = await openai.createCompletion({
    model: "text-davinci-003",
    prompt: `Decide whether a Tweet\'s is chosen color. then reply with the color only.\n\nTweet: "${prompt}"\n\n`,
    temperature: 0,
    max_tokens: 60,
    top_p: 1,
    frequency_penalty: 0.5,
    presence_penalty: 0,
  });
  return response.data.choices[0].text;
};

export const decideQuestionStartEngine = async (prompt) => {
  const response = await openai.createCompletion({
    model: "text-davinci-003",
    prompt: `Decide whether a Tweet\'s is asking to start engine. then reply with true or false.\n\nTweet: "${prompt}"\n\n`,
    temperature: 0,
    max_tokens: 60,
    top_p: 1,
    frequency_penalty: 0.5,
    presence_penalty: 0,
  });
  return response.data.choices[0].text;
};

export const decideToMoveArm = async (prompt) => {
  const response = await openai.createCompletion({
    model: "text-davinci-003",
    prompt: `Decide whether a Tweet\'s is asking to move arm. then reply with true or false.\n\nTweet: "${prompt}"\n\n`,
    temperature: 0,
    max_tokens: 60,
    top_p: 1,
    frequency_penalty: 0.5,
    presence_penalty: 0,
  });
  return response.data.choices[0].text;
};

export const decideToMoveToBase = async (prompt) => {
  const response = await openai.createCompletion({
    model: "text-davinci-003",
    prompt: `Decide whether a Tweet\'s is asking the robot arm to move to base. then reply with true or false.\n\nTweet: "${prompt}"\n\n`,
    temperature: 0,
    max_tokens: 60,
    top_p: 1,
    frequency_penalty: 0.5,
    presence_penalty: 0,
  });
  return response.data.choices[0].text;
};
