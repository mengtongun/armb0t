export const START_ENGINE = "engine:true";
export const MOVE_ARM = "arm:true";
export const CHOOSE_COLOR = "color:";
export const MOVE_BASE = "base:true";
export const PICK_RED = "color:red";
export const PICK_BLUE = "color:blue";
export const PICK_GREEN = "color:green";
export const PICK_YELLOW = "color:yellow";
export const replyStartEngine = async (prompt) => {
  return prompt.toLowerCase().includes("start engine");
};
