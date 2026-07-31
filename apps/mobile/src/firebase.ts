import { initializeApp } from "firebase/app";

const firebaseConfig = {
  apiKey: "AIzaSyAvHJIBNByTcfoy3K4W7XnOQv19rjamWew",
  authDomain: "agrovision-6bac6.firebaseapp.com",
  projectId: "agrovision-6bac6",
  storageBucket: "agrovision-6bac6.firebasestorage.app",
  messagingSenderId: "17354140213",
  appId: "1:17354140213:web:82d6b6e889c45384ad5f7c",
  measurementId: "G-EXVLF5KHSF"
};

export const app = initializeApp(firebaseConfig);