import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card } from "@/components/ui/card";
import { Zap, RotateCcw } from "lucide-react";

interface CodeAnalysisFormProps {
  onAnalyze: (code: string, errorMessage: string, language?: string) => void;
  isLoading: boolean;
  onReset: () => void;
}

const LANGUAGES = [
  "Auto-detect",
  "JavaScript",
  "TypeScript",
  "Python",
  "Java",
  "C",
  "C++",
  "Go",
  "Rust",
  "Ruby",
  "PHP",
];

export const CodeAnalysisForm = ({ onAnalyze, isLoading, onReset }: CodeAnalysisFormProps) => {
  const [code, setCode] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [language, setLanguage] = useState("Auto-detect");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (code.trim() && errorMessage.trim()) {
      onAnalyze(
        code, 
        errorMessage, 
        language === "Auto-detect" ? undefined : language
      );
    }
  };

  const handleClear = () => {
    setCode("");
    setErrorMessage("");
    setLanguage("Auto-detect");
    onReset();
  };

  const isValid = code.trim().length > 0 && errorMessage.trim().length > 0;

  return (
    <Card className="p-6 bg-card border-border">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Code Input */}
        <div className="space-y-2">
          <Label htmlFor="code" className="text-foreground font-medium">
            Your Code
          </Label>
          <Textarea
            id="code"
            placeholder="Paste your buggy code here..."
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="min-h-[200px] font-mono text-sm bg-code-bg text-code-fg border-border resize-y"
            disabled={isLoading}
          />
          <p className="text-xs text-muted-foreground">
            Enter the code snippet that's causing issues
          </p>
        </div>

        {/* Error Message Input */}
        <div className="space-y-2">
          <Label htmlFor="error" className="text-foreground font-medium">
            Error Message
          </Label>
          <Textarea
            id="error"
            placeholder="Paste the error message or stack trace here..."
            value={errorMessage}
            onChange={(e) => setErrorMessage(e.target.value)}
            className="min-h-[120px] font-mono text-sm bg-code-bg text-code-fg border-border resize-y"
            disabled={isLoading}
          />
          <p className="text-xs text-muted-foreground">
            Include the complete error message for better analysis
          </p>
        </div>

        {/* Language Selector */}
        <div className="space-y-2">
          <Label htmlFor="language" className="text-foreground font-medium">
            Programming Language (Optional)
          </Label>
          <Select value={language} onValueChange={setLanguage} disabled={isLoading}>
            <SelectTrigger id="language" className="bg-background border-border">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-popover border-border">
              {LANGUAGES.map((lang) => (
                <SelectItem key={lang} value={lang}>
                  {lang}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <p className="text-xs text-muted-foreground">
            Helps provide more accurate analysis
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <Button
            type="submit"
            disabled={!isValid || isLoading}
            className="flex-1 bg-primary text-primary-foreground hover:bg-primary/90"
          >
            <Zap className="mr-2 h-4 w-4" />
            {isLoading ? "Analyzing..." : "Analyze Code"}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={handleClear}
            disabled={isLoading}
            className="border-border hover:bg-muted"
          >
            <RotateCcw className="h-4 w-4" />
          </Button>
        </div>
      </form>
    </Card>
  );
};
