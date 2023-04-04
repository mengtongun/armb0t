const piDetectionServer = "http://localhost:3002";

export const detectedColors = async () => {
  try {
    const response = await fetch("http://localhost:3002");
    return response.json();
  } catch (error) {
    return error;
  }
};
