import { Card } from "@/components/ui/card";
import { Code2, ArrowLeft, Sparkles } from "lucide-react";

export const EmptyState = () => {
  return (
    <Card className="p-12 bg-card border-border flex flex-col items-center justify-center space-y-6 min-h-[400px]">
      <div className="relative">
        <div className="p-4 rounded-2xl bg-primary/10 border border-primary/20">
          <Code2 className="h-12 w-12 text-primary" />
        </div>
        <Sparkles className="h-6 w-6 text-accent absolute -top-1 -right-1" />
      </div>
      
      <div className="text-center space-y-3 max-w-md">
        <h3 className="text-2xl font-bold text-foreground">Ready to Debug</h3>
        <p className="text-muted-foreground leading-relaxed">
          Paste your buggy code and error message on the left to get started. Our AI will analyze your code
          and provide clear explanations and suggested fixes.
        </p>
      </div>

      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <ArrowLeft className="h-4 w-4" />
        <span>Enter your code and error message to begin</span>
      </div>

      <div className="pt-6 border-t border-border w-full max-w-md">
        <div className="space-y-3">
          <p className="text-sm font-medium text-foreground text-center">What we analyze:</p>
          <div className="grid grid-cols-2 gap-3 text-xs text-muted-foreground">
            <div className="flex items-center gap-2">
              <div className="h-1.5 w-1.5 rounded-full bg-primary" />
              <span>Syntax errors</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-1.5 w-1.5 rounded-full bg-primary" />
              <span>Runtime errors</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-1.5 w-1.5 rounded-full bg-primary" />
              <span>Logic bugs</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-1.5 w-1.5 rounded-full bg-primary" />
              <span>Type errors</span>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};
