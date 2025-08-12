import { View, Text } from "react-native";
import { QueryClient, QueryClientProvider } from "react-query";
const queryClient = new QueryClient();
export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <View className="flex-1 items-center justify-center bg-gray-100">
        <Text className="text-xl font-bold text-blue-600">
          TaskHub Mobile — Hello World!
        </Text>
      </View>
    </QueryClientProvider>
  );
}
