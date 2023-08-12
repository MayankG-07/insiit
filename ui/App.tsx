import { useState } from "react";
import {
  Button,
  Image,
  ImageBackground,
  Modal,
  Pressable,
  ScrollView,
  Text,
  View,
  StatusBar,
  ActivityIndicator,
  Alert,
} from "react-native";

const logo = require("./assets/adaptive-icon.png");

const App = () => {
  const [isStatusBarVisible, setIsStatusBarVisible] = useState(false);

  return (
    <View
      style={{
        flex: 1,
        backgroundColor: "plum",
        padding: 60,
      }}
    >
      <Button
        title="Alert"
        onPress={() =>
          Alert.alert("Invalid data", "Date of birth is incorrect", [
            { text: "Cancel", onPress: () => console.log("cancel pressed") },
            { text: "Ok", onPress: () => console.log("ok pressed") },
          ])
        }
      />
    </View>
  );
};

export default App;
