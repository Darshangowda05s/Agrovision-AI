import React, { useState, useRef } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  ScrollView,
  Animated,
  Dimensions,
  StatusBar,
} from "react-native";
import * as ImagePicker from "expo-image-picker";

const { width } = Dimensions.get("window");
type Props = {
  onAnalyze: () => void;
};

export default function HomeScreen({
  onAnalyze,
}: Props) {
  const [images, setImages] = useState<string[]>([]);
  const [analyzing, setAnalyzing] = useState(false);

  const pulseAnim = useRef(new Animated.Value(1)).current;

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ["images"],
      allowsMultipleSelection: true,
      quality: 1,
    });

    if (!result.canceled) {
      setImages(result.assets.map((asset) => asset.uri));
    }
  };

  const takePhoto = async () => {
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ["images"],
      quality: 1,
    });

    if (!result.canceled) {
      setImages([result.assets[0].uri]);
    }
  };

  const handleAnalyze = () => {
  setAnalyzing(true);

  setTimeout(() => {
    setAnalyzing(false);
    onAnalyze(); // Navigate to Result Screen
  }, 2000);
};

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      showsVerticalScrollIndicator={false}
    >
      <StatusBar
        backgroundColor="#F4F8F2"
        barStyle="dark-content"
      />

      {/* Header */}

      <View style={styles.header}>
        <View style={styles.badge}>
          <Text style={styles.badgeText}>AI Powered</Text>
        </View>

        <Text style={styles.title}>AgroVision</Text>

        <Text style={styles.subtitle}>
          Detect plant diseases instantly and get
          treatment recommendations.
        </Text>
      </View>

      {/* Steps */}

      <View style={styles.stepsCard}>
        <View style={styles.step}>
          <Text style={styles.stepNumber}>1</Text>
          <Text style={styles.stepText}>Upload</Text>
        </View>

        <Text style={styles.arrow}>→</Text>

        <View style={styles.step}>
          <Text style={styles.stepNumber}>2</Text>
          <Text style={styles.stepText}>Analyze</Text>
        </View>

        <Text style={styles.arrow}>→</Text>

        <View style={styles.step}>
          <Text style={styles.stepNumber}>3</Text>
          <Text style={styles.stepText}>Treatment</Text>
        </View>
      </View>

      {/* Features */}

      <View style={styles.featuresRow}>
        <View style={styles.featureCard}>
          <Text style={styles.featureIcon}>🌿</Text>
          <Text style={styles.featureText}>
            15+ Diseases
          </Text>
        </View>

        <View style={styles.featureCard}>
          <Text style={styles.featureIcon}>⚡</Text>
          <Text style={styles.featureText}>
            Fast Analysis
          </Text>
        </View>

        <View style={styles.featureCard}>
          <Text style={styles.featureIcon}>📷</Text>
          <Text style={styles.featureText}>
            Multi Photos
          </Text>
        </View>
      </View>

      {/* Upload Card */}

      <View style={styles.uploadCard}>
        <Text style={styles.uploadTitle}>
          Upload Leaf Photos
        </Text>

        <Text style={styles.uploadSubtitle}>
          Take a clear photo of the affected leaf.
          You can upload up to 10 photos.
        </Text>

        {/* Camera Button */}

        <TouchableOpacity
          style={styles.primaryButton}
          onPress={takePhoto}
        >
          <Text style={styles.primaryButtonText}>
            📸 Take Photo
          </Text>
        </TouchableOpacity>

        {/* Gallery Button */}

        <TouchableOpacity
          style={styles.secondaryButton}
          onPress={pickImage}
        >
          <Text style={styles.secondaryButtonText}>
            🖼️ Choose From Gallery
          </Text>
        </TouchableOpacity>

        {/* Tips */}

        <View style={styles.tipsContainer}>
          <Text style={styles.tip}>
            ✓ Keep leaf in focus
          </Text>

          <Text style={styles.tip}>
            ✓ Use daylight if possible
          </Text>

          <Text style={styles.tip}>
            ✓ One leaf per photo
          </Text>
        </View>
      </View>

      {/* Selected Images */}

      {images.length > 0 && (
        <View style={styles.previewCard}>
          <Text style={styles.previewTitle}>
            {images.length} Photo
            {images.length > 1 ? "s" : ""} Selected
          </Text>

          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
          >
            {images.map((uri, index) => (
              <Image
                key={index}
                source={{ uri }}
                style={styles.previewImage}
              />
            ))}
          </ScrollView>
        </View>
      )}

      {/* Analyze */}

      {images.length > 0 && (
        <Animated.View
          style={{
            width: "100%",
            transform: [{ scale: pulseAnim }],
          }}
        >
          <TouchableOpacity
            style={styles.analyzeButton}
            onPress={handleAnalyze}
            disabled={analyzing}
          >
            <Text style={styles.analyzeText}>
              {analyzing
                ? "Analyzing..."
                : "🔬 Analyze Disease"}
            </Text>
          </TouchableOpacity>
        </Animated.View>
      )}

      {/* Footer */}

      <Text style={styles.footer}>
        Helping farmers detect crop diseases early.
      </Text>
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
    marginBottom: 25,
  },

  badge: {
    alignSelf: "flex-start",
    backgroundColor: "#E8F5E9",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 30,
    marginBottom: 12,
  },

  badgeText: {
    color: "#2E7D32",
    fontWeight: "700",
  },

  title: {
    fontSize: 40,
    fontWeight: "800",
    color: "#1B1B1B",
  },

  subtitle: {
    fontSize: 16,
    color: "#5F6368",
    marginTop: 8,
    lineHeight: 24,
  },

  stepsCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 18,
    padding: 18,
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
    marginBottom: 18,
    elevation: 2,
  },

  step: {
    alignItems: "center",
  },

  stepNumber: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: "#2E7D32",
    color: "#fff",
    textAlign: "center",
    lineHeight: 36,
    fontWeight: "700",
  },

  stepText: {
    marginTop: 6,
    color: "#1B1B1B",
    fontWeight: "600",
  },

  arrow: {
    fontSize: 22,
    color: "#2E7D32",
  },

  featuresRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 20,
  },

  featureCard: {
    width: "31%",
    backgroundColor: "#FFFFFF",
    borderRadius: 16,
    padding: 14,
    alignItems: "center",
  },

  featureIcon: {
    fontSize: 24,
    marginBottom: 6,
  },

  featureText: {
    fontSize: 12,
    fontWeight: "600",
    textAlign: "center",
  },

  uploadCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 22,
    padding: 20,
    marginBottom: 20,
  },

  uploadTitle: {
    fontSize: 24,
    fontWeight: "800",
    color: "#1B1B1B",
    marginBottom: 8,
  },

  uploadSubtitle: {
    color: "#5F6368",
    lineHeight: 22,
    marginBottom: 20,
  },

  primaryButton: {
    backgroundColor: "#2E7D32",
    paddingVertical: 18,
    borderRadius: 14,
    alignItems: "center",
    marginBottom: 12,
  },

  primaryButtonText: {
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: 17,
  },

  secondaryButton: {
    borderWidth: 2,
    borderColor: "#2E7D32",
    paddingVertical: 18,
    borderRadius: 14,
    alignItems: "center",
  },

  secondaryButtonText: {
    color: "#2E7D32",
    fontWeight: "700",
    fontSize: 17,
  },

  tipsContainer: {
    marginTop: 20,
  },

  tip: {
    color: "#2E7D32",
    marginBottom: 8,
    fontSize: 15,
  },

  previewCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 20,
    padding: 18,
    marginBottom: 20,
  },

  previewTitle: {
    fontSize: 18,
    fontWeight: "700",
    marginBottom: 14,
  },

  previewImage: {
    width: 130,
    height: 130,
    borderRadius: 16,
    marginRight: 10,
  },

  analyzeButton: {
    backgroundColor: "#2E7D32",
    paddingVertical: 20,
    borderRadius: 18,
    alignItems: "center",
  },

  analyzeText: {
    color: "#FFFFFF",
    fontWeight: "800",
    fontSize: 18,
  },

  footer: {
    textAlign: "center",
    color: "#5F6368",
    marginTop: 24,
    fontSize: 14,
  },
});