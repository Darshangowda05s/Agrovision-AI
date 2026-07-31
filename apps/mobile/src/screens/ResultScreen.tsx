import React from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  StatusBar,
} from "react-native";

type Props = {
  onBack: () => void;
};

export default function ResultScreen({
  onBack,
}: Props) {
  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
    >
      <StatusBar
        backgroundColor="#F4F8F2"
        barStyle="dark-content"
      />

      <Text style={styles.header}>
        Analysis Result
      </Text>

      <View style={styles.diseaseCard}>
        <Text style={styles.diseaseIcon}>
          
        </Text>

        <Text style={styles.label}>
          Disease Detected
        </Text>

        <Text style={styles.diseaseName}>
          Disease type
        </Text>
      </View>

      <View style={styles.infoCard}>
        <Text style={styles.infoTitle}>
          Confidence
        </Text>

        <Text style={styles.infoValue}>
          
        </Text>
      </View>

      <View style={styles.infoCard}>
        <Text style={styles.infoTitle}>
          Severity
        </Text>

        <Text style={styles.infoValue}>
          Low/Medium/High
        </Text>
      </View>

      <View style={styles.treatmentCard}>
        <Text style={styles.sectionTitle}>
           Recommended Treatment
        </Text>

        <Text style={styles.sectionText}>
          Recommended treatment based on the detected disease.
        </Text>
      </View>

      <View style={styles.treatmentCard}>
        <Text style={styles.sectionTitle}>
           Prevention Tips
        </Text>

        <Text style={styles.tip}>
          • Tips to prevent the disease from spreading to other plants.
        </Text>


      </View>

      <View style={styles.treatmentCard}>
        <Text style={styles.sectionTitle}>
          📅 Recheck Crop
        </Text>

        <Text style={styles.sectionText}>
          Check again after 5 days.
        </Text>
      </View>

      <TouchableOpacity
        style={styles.button}
        onPress={onBack}
      >
        <Text style={styles.buttonText}>
          Analyze Another Leaf
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F4F8F2",
  },

  content: {
    padding: 20,
    paddingTop: 60,
    paddingBottom: 40,
  },

  header: {
    fontSize: 30,
    fontWeight: "800",
    color: "#1B1B1B",
    marginBottom: 20,
    textAlign: "center",
  },

  diseaseCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 20,
    padding: 24,
    alignItems: "center",
    marginBottom: 20,
  },

  diseaseIcon: {
    fontSize: 50,
  },

  label: {
    color: "#5F6368",
    marginTop: 10,
  },

  diseaseName: {
    fontSize: 28,
    fontWeight: "800",
    color: "#D32F2F",
    marginTop: 8,
  },

  infoCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 16,
    padding: 18,
    marginBottom: 15,
  },

  infoTitle: {
    color: "#5F6368",
    marginBottom: 6,
  },

  infoValue: {
    fontSize: 24,
    fontWeight: "700",
    color: "#2E7D32",
  },

  treatmentCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 16,
    padding: 18,
    marginBottom: 15,
  },

  sectionTitle: {
    fontSize: 18,
    fontWeight: "700",
    marginBottom: 10,
  },

  sectionText: {
    color: "#333",
    lineHeight: 22,
  },

  tip: {
    marginBottom: 8,
    color: "#333",
  },

  button: {
    backgroundColor: "#2E7D32",
    paddingVertical: 18,
    borderRadius: 16,
    alignItems: "center",
    marginTop: 10,
  },

  buttonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
});