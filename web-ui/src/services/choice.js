export const START_ENGINE = "engine:true";
export const MOVE_ARM = "arm:true";
export const CHOOSE_COLOR = "color:";
export const MOVE_BASE = "base:true";

export const replyStartEngine = async (prompt) => {
  return prompt.toLowerCase().includes("start engine");
};
