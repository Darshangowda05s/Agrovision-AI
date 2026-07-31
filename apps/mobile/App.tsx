import React, { useState } from "react";

import LoginScreen from "./src/screens/LoginScreen";
import HomeScreen from "./src/screens/HomeScreen";
import ResultScreen from "./src/screens/ResultScreen";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [showResult, setShowResult] = useState(false);

  if (!loggedIn) {
    return (
      <LoginScreen onLogin={() => setLoggedIn(true)} />
    );
  }

  if (showResult) {
    return (
      <ResultScreen
        onBack={() => setShowResult(false)}
      />
    );
  }

  return (
    <HomeScreen
      onAnalyze={() => setShowResult(true)}
    />
  );
}