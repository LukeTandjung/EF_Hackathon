import { useState, useEffect } from "react";
import { Case, Message, Juror } from "@/types";
import CaseInput from "@/components/CaseInput";
import JurorConfiguration from "@/components/JurorConfiguration";
import JuryPanel from "@/components/JuryPanel";
import Discussion from "@/components/Discussion";
import VerdictTracker from "@/components/VerdictTracker";
import MacroStats from "@/components/MacroStats";
import { useToast } from "@/hooks/use-toast";

interface SimulationResult {
  jurors: Juror[];
  id: number;
  messages: Message[];
}

const Index = () => {
  const [caseData, setCaseData] = useState<Case | null>(null);
  const [simulations, setSimulations] = useState<SimulationResult[]>([]);
  const [showJurorConfig, setShowJurorConfig] = useState(false);
  const { toast } = useToast();

  const generateNextMessage = (currentCase: Case, simulation: SimulationResult) => {
    const availableJurors = simulation.jurors.filter(j => 
      !simulation.messages.slice(-2).some(m => m.jurorId === j.id)
    );
    const nextJuror = availableJurors[Math.floor(Math.random() * availableJurors.length)];
    
    const messageTemplates = [
      `I've reviewed the ${currentCase.title} case carefully. The prosecution's argument about ${currentCase.prosecution.slice(0, 50)}... is compelling.`,
      `Looking at the defense's position regarding ${currentCase.defense.slice(0, 50)}..., we need to consider all angles.`,
      "Based on the evidence presented, I'm leaning towards a not-guilty verdict.",
      "The prosecution has made some strong points that we can't ignore.",
      "We need to carefully weigh both sides before making our decision.",
      "Let's examine the key evidence one more time."
    ];

    return {
      id: simulation.messages.length + 1,
      jurorId: nextJuror.id,
      content: messageTemplates[Math.floor(Math.random() * messageTemplates.length)],
      timestamp: new Date()
    };
  };

  useEffect(() => {
    if (caseData && simulations.length > 0) {
      const timer = setInterval(() => {
        setSimulations(prevSimulations => 
          prevSimulations.map(sim => {
            const newMessage = generateNextMessage(caseData, sim);
            
            // Update juror votes every 3 messages
            const updatedJurors = sim.messages.length % 3 === 0
              ? sim.jurors.map(juror => ({
                  ...juror,
                  currentVote: (Math.random() > 0.5 ? "guilty" : "not-guilty") as const
                }))
              : sim.jurors;

            return {
              ...sim,
              messages: [...sim.messages, newMessage],
              jurors: updatedJurors,
            };
          })
        );
      }, 3000);

      return () => clearInterval(timer);
    }
  }, [caseData, simulations]);

  const handleCaseSubmit = (newCase: Case) => {
    setCaseData(newCase);
    setShowJurorConfig(true);
  };

  const handleJurorSubmit = (configuredSimulations: { jurors: Juror[]; id: number }[]) => {
    setShowJurorConfig(false);
    const initializedSimulations = configuredSimulations.map(sim => ({
      ...sim,
      messages: [{
        id: 1,
        jurorId: sim.jurors[0].id,
        content: "Let's begin our deliberation. First, let's review the key points of the case.",
        timestamp: new Date(),
      }],
    }));
    setSimulations(initializedSimulations);
    
    toast({
      title: "Simulations Started",
      description: `Running ${configuredSimulations.length} jury deliberations simultaneously.`,
    });
  };

  return (
    <div className="min-h-screen bg-parchment py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-crimson font-bold text-navy mb-4">
            AI Jury Deliberation
          </h1>
          <p className="text-lg text-gray-600">
            Experience multiple simulated jury discussions powered by AI
          </p>
        </header>

        {!caseData ? (
          <CaseInput onSubmit={handleCaseSubmit} />
        ) : showJurorConfig ? (
          <JurorConfiguration onSubmit={handleJurorSubmit} />
        ) : (
          <div className="space-y-8">
            <MacroStats simulations={simulations} />
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {simulations.slice(0, 4).map(simulation => (
                <div key={simulation.id} className="space-y-8">
                  <h2 className="text-xl font-crimson font-bold">Simulation {simulation.id}</h2>
                  <Discussion messages={simulation.messages} jurors={simulation.jurors} />
                  <VerdictTracker jurors={simulation.jurors} />
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Index;