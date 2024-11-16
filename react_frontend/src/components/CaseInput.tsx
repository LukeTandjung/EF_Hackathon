import { useState } from "react";
import { Case } from "@/types";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";

interface CaseInputProps {
  onSubmit: (caseData: Case) => void;
}

const CaseInput = ({ onSubmit }: CaseInputProps) => {
  const [caseData, setCaseData] = useState<Case>({
    title: "",
    description: "",
    prosecution: "",
    defense: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(caseData);
  };

  return (
    <Card className="p-6 bg-white shadow-lg">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-lg font-crimson mb-2">
            Case Title
          </label>
          <Input
            id="title"
            value={caseData.title}
            onChange={(e) => setCaseData({ ...caseData, title: e.target.value })}
            placeholder="Enter case title..."
            className="w-full"
            required
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-lg font-crimson mb-2">
            Case Description
          </label>
          <Textarea
            id="description"
            value={caseData.description}
            onChange={(e) => setCaseData({ ...caseData, description: e.target.value })}
            placeholder="Describe the case..."
            className="w-full min-h-[100px]"
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="prosecution" className="block text-lg font-crimson mb-2">
              Prosecution Arguments
            </label>
            <Textarea
              id="prosecution"
              value={caseData.prosecution}
              onChange={(e) => setCaseData({ ...caseData, prosecution: e.target.value })}
              placeholder="Enter prosecution's key points..."
              className="w-full min-h-[100px]"
              required
            />
          </div>

          <div>
            <label htmlFor="defense" className="block text-lg font-crimson mb-2">
              Defense Arguments
            </label>
            <Textarea
              id="defense"
              value={caseData.defense}
              onChange={(e) => setCaseData({ ...caseData, defense: e.target.value })}
              placeholder="Enter defense's key points..."
              className="w-full min-h-[100px]"
              required
            />
          </div>
        </div>

        <Button
          type="submit"
          className="w-full bg-navy hover:bg-navy-light text-white font-semibold py-2 px-4 rounded transition-colors"
        >
          Begin Jury Deliberation
        </Button>
      </form>
    </Card>
  );
};

export default CaseInput;