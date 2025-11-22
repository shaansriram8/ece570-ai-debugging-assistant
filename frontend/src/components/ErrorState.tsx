import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { AlertTriangle, RefreshCcw } from "lucide-react";

interface ErrorStateProps {
  error: string;
  onRetry: () => void;
}

export const ErrorState = ({ error, onRetry }: ErrorStateProps) => {
  return (
    <Card className="p-12 bg-card border-destructive/50 flex flex-col items-center justify-center space-y-6 min-h-[400px]">
      <div className="p-4 rounded-2xl bg-destructive/10 border border-destructive/20">
        <AlertTriangle className="h-12 w-12 text-destructive" />
      </div>
      
      <div className="text-center space-y-3 max-w-md">
        <h3 className="text-2xl font-bold text-foreground">Analysis Failed</h3>
        <p className="text-muted-foreground leading-relaxed">{error}</p>
      </div>

      <Button
        onClick={onRetry}
        variant="outline"
        className="border-border hover:bg-muted"
      >
        <RefreshCcw className="mr-2 h-4 w-4" />
        Try Again
      </Button>

      <div className="pt-6 border-t border-border w-full max-w-md">
        <div className="space-y-2 text-sm text-muted-foreground">
          <p className="font-medium text-foreground text-center">Troubleshooting Tips:</p>
          <ul className="space-y-1 text-xs">
            <li>• Check your internet connection</li>
            <li>• Ensure the backend service is running</li>
            <li>• Verify your inputs are properly formatted</li>
            <li>• Try again with a different code sample</li>
          </ul>
        </div>
      </div>
    </Card>
  );
};
