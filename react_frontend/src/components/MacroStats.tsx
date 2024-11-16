import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Juror } from "@/types";

interface SimulationResult {
  jurors: Juror[];
  id: number;
}

interface MacroStatsProps {
  simulations: SimulationResult[];
}

const MacroStats = ({ simulations }: MacroStatsProps) => {
  const totalSimulations = simulations.length;
  
  const getVerdict = (jurors: Juror[]) => {
    const guiltyCount = jurors.filter(j => j.currentVote === "guilty").length;
    const notGuiltyCount = jurors.filter(j => j.currentVote === "not-guilty").length;
    const total = jurors.length;
    
    if (guiltyCount >= total * 0.75) return "guilty";
    if (notGuiltyCount >= total * 0.75) return "not-guilty";
    return "hung";
  };

  const verdicts = simulations.map(sim => getVerdict(sim.jurors));
  const guiltyCount = verdicts.filter(v => v === "guilty").length;
  const notGuiltyCount = verdicts.filter(v => v === "not-guilty").length;
  const hungCount = verdicts.filter(v => v === "hung").length;

  return (
    <Card className="p-6 bg-white shadow-lg">
      <h2 className="text-2xl font-crimson mb-4">Macro Statistics</h2>
      
      <div className="space-y-4">
        <div>
          <div className="flex justify-between mb-2">
            <span className="font-semibold text-burgundy">Guilty Verdicts</span>
            <span className="text-burgundy">{guiltyCount}/{totalSimulations}</span>
          </div>
          <Progress value={(guiltyCount / totalSimulations) * 100} className="bg-gray-200 h-2" />
        </div>

        <div>
          <div className="flex justify-between mb-2">
            <span className="font-semibold text-navy">Not Guilty Verdicts</span>
            <span className="text-navy">{notGuiltyCount}/{totalSimulations}</span>
          </div>
          <Progress value={(notGuiltyCount / totalSimulations) * 100} className="bg-gray-200 h-2" />
        </div>

        <div>
          <div className="flex justify-between mb-2">
            <span className="font-semibold text-gray-600">Hung Juries</span>
            <span className="text-gray-600">{hungCount}/{totalSimulations}</span>
          </div>
          <Progress value={(hungCount / totalSimulations) * 100} className="bg-gray-200 h-2" />
        </div>
      </div>
    </Card>
  );
};

export default MacroStats;