import * as Speech from "expo-speech";

export const speakKannada = (text: string) => {
  Speech.speak(text, {
    language: "kn-IN",
    pitch: 1,
    rate: 0.9,
  });
};

export const stopSpeaking = () => {
  Speech.stop();
};