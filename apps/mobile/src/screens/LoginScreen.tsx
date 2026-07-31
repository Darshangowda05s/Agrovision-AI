import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  StatusBar,
  Alert,
} from "react-native";

type Props = {
  onLogin: () => void;
};

export default function LoginScreen({ onLogin }: Props) {
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);

  const handleSendOtp = () => {
    if (phone.length !== 10) {
      Alert.alert("Invalid Number", "Enter a valid 10-digit mobile number");
      return;
    }

    setOtpSent(true);

    Alert.alert(
      "OTP Sent",
      "For demo, use OTP: 123456"
    );
  };

  const handleVerifyOtp = () => {
    if (otp === "123456") {
      onLogin();
    } else {
      Alert.alert("Invalid OTP", "Please enter correct OTP");
    }
  };

  return (
    <View style={styles.container}>
      <StatusBar
        backgroundColor="#F4F8F2"
        barStyle="dark-content"
      />

      <Text style={styles.logo}>🌾</Text>

      <Text style={styles.title}>AgroVision</Text>

      <Text style={styles.subtitle}>
        AI Disease Detection for Farmers
      </Text>

      <View style={styles.card}>
        {!otpSent ? (
          <>
            <Text style={styles.label}>
              Mobile Number
            </Text>

            <TextInput
              style={styles.input}
              placeholder="9876543210"
              keyboardType="phone-pad"
              value={phone}
              onChangeText={setPhone}
              maxLength={10}
            />

            <TouchableOpacity
              style={styles.button}
              onPress={handleSendOtp}
            >
              <Text style={styles.buttonText}>
                Send OTP
              </Text>
            </TouchableOpacity>
          </>
        ) : (
          <>
            <Text style={styles.label}>
              Verification Code
            </Text>

            <Text style={styles.otpInfo}>
              OTP sent to +91 {phone}
            </Text>

            <TextInput
              style={styles.input}
              placeholder="Enter OTP"
              keyboardType="number-pad"
              value={otp}
              onChangeText={setOtp}
              maxLength={6}
            />

            <TouchableOpacity
              style={styles.button}
              onPress={handleVerifyOtp}
            >
              <Text style={styles.buttonText}>
                Verify OTP
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              onPress={() => setOtpSent(false)}
            >
              <Text style={styles.changeNumber}>
                Change Number
              </Text>
            </TouchableOpacity>
          </>
        )}

        <Text style={styles.info}>
          ✓ Free to use
        </Text>

        <Text style={styles.info}>
          ✓ Instant disease detection
        </Text>

        <Text style={styles.info}>
          ✓ Treatment recommendations
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F4F8F2",
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },

  logo: {
    fontSize: 60,
  },

  title: {
    fontSize: 36,
    fontWeight: "800",
    color: "#1B1B1B",
    marginTop: 10,
  },

  subtitle: {
    color: "#5F6368",
    fontSize: 16,
    marginBottom: 30,
  },

  card: {
    width: "100%",
    backgroundColor: "#FFF",
    borderRadius: 20,
    padding: 20,
  },

  label: {
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 10,
  },

  input: {
    borderWidth: 1,
    borderColor: "#DDD",
    borderRadius: 12,
    paddingHorizontal: 15,
    height: 55,
    marginBottom: 20,
    fontSize: 16,
  },

  button: {
    backgroundColor: "#2E7D32",
    height: 55,
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 15,
  },

  buttonText: {
    color: "#FFF",
    fontWeight: "700",
    fontSize: 16,
  },

  otpInfo: {
    color: "#5F6368",
    marginBottom: 15,
  },

  changeNumber: {
    color: "#2E7D32",
    textAlign: "center",
    marginBottom: 15,
    fontWeight: "600",
  },

  info: {
    color: "#2E7D32",
    marginTop: 8,
  },
});