import { Card } from "@/components/ui/card";
import { Loader2, Brain } from "lucide-react";

export const LoadingState = () => {
  return (
    <Card className="p-12 bg-card border-border flex flex-col items-center justify-center space-y-4 min-h-[400px]">
      <div className="relative">
        <Brain className="h-16 w-16 text-primary animate-pulse" />
        <Loader2 className="h-8 w-8 text-accent absolute -bottom-2 -right-2 animate-spin" />
      </div>
      <div className="text-center space-y-2">
        <h3 className="text-xl font-semibold text-foreground">Analyzing Your Code</h3>
        <p className="text-muted-foreground">
          Our AI models are examining your code and error message...
        </p>
      </div>
      <div className="flex gap-2 mt-4">
        <div className="h-2 w-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
        <div className="h-2 w-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
        <div className="h-2 w-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
      </div>
    </Card>
  );
};
