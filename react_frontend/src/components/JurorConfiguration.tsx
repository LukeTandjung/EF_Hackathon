import { useState } from "react";
import { Juror } from "@/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { JurorForm } from "./JurorForm";

interface JurorConfigurationProps {
  onSubmit: (simulations: { jurors: Juror[]; id: number }[]) => void;
}

const JurorConfiguration = ({ onSubmit }: JurorConfigurationProps) => {
  const [simulationCount, setSimulationCount] = useState(5);
  const [jurorCount, setJurorCount] = useState(5);
  const [baseJurors, setBaseJurors] = useState<Juror[]>(() => 
    Array.from({ length: jurorCount }, (_, i) => ({
      id: i + 1,
      name: `Juror ${i + 1}`,
      personality: {
        openness: 50,
        conscientiousness: 50,
        extraversion: 50,
        agreeableness: 50,
        neuroticism: 50,
      },
      avatar: "👤",
      currentVote: "undecided" as const,
      gender: "Prefer not to say",
      race: "Prefer not to say",
      politicalBelief: "Independent",
      religion: "Prefer not to say",
    }))
  );

  const handleJurorCountChange = (count: number) => {
    setJurorCount(count);
    if (count > baseJurors.length) {
      const newJurors = Array.from({ length: count - baseJurors.length }, (_, i) => ({
        id: baseJurors.length + i + 1,
        name: `Juror ${baseJurors.length + i + 1}`,
        personality: {
          openness: 50,
          conscientiousness: 50,
          extraversion: 50,
          agreeableness: 50,
          neuroticism: 50,
        },
        avatar: "👤",
        currentVote: "undecided" as const,
        gender: "Prefer not to say",
        race: "Prefer not to say",
        politicalBelief: "Independent",
        religion: "Prefer not to say",
      }));
      setBaseJurors([...baseJurors, ...newJurors]);
    } else {
      setBaseJurors(baseJurors.slice(0, count));
    }
  };

  const randomizeJuror = (juror: Juror): Juror => ({
    ...juror,
    personality: {
      openness: Math.floor(Math.random() * 100),
      conscientiousness: Math.floor(Math.random() * 100),
      extraversion: Math.floor(Math.random() * 100),
      agreeableness: Math.floor(Math.random() * 100),
      neuroticism: Math.floor(Math.random() * 100),
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const simulations = Array.from({ length: simulationCount }, (_, simIndex) => ({
      id: simIndex + 1,
      jurors: baseJurors.map(juror => randomizeJuror({ ...juror })),
    }));
    onSubmit(simulations);
  };

  return (
    <Card className="p-6 bg-white shadow-lg">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-lg font-semibold mb-2">Number of Simulations</label>
            <Input
              type="number"
              min="1"
              max="100"
              value={simulationCount}
              onChange={(e) => setSimulationCount(parseInt(e.target.value))}
              className="w-full"
            />
          </div>
          <div>
            <label className="block text-lg font-semibold mb-2">Jurors per Simulation</label>
            <Input
              type="number"
              min="3"
              max="12"
              value={jurorCount}
              onChange={(e) => handleJurorCountChange(parseInt(e.target.value))}
              className="w-full"
            />
          </div>
        </div>

        <ScrollArea className="h-[400px] pr-4">
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Base Juror Templates</h3>
            <p className="text-sm text-gray-600 mb-4">
              These templates will be randomized for each simulation while maintaining the basic characteristics.
            </p>
            {baseJurors.map((juror, index) => (
              <JurorForm 
                key={juror.id} 
                juror={juror} 
                index={index}
                onChange={(updates) => {
                  const newJurors = [...baseJurors];
                  newJurors[index] = { ...newJurors[index], ...updates };
                  setBaseJurors(newJurors);
                }}
              />
            ))}
          </div>
        </ScrollArea>

        <Button type="submit" className="w-full">
          Start {simulationCount} Simulations
        </Button>
      </form>
    </Card>
  );
};

export default JurorConfiguration;