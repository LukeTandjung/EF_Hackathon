import { Juror } from "@/types";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

interface VerdictTrackerProps {
  jurors: Juror[];
}

const VerdictTracker = ({ jurors }: VerdictTrackerProps) => {
  const totalJurors = jurors.length;
  const guiltyCount = jurors.filter((j) => j.currentVote === "guilty").length;
  const notGuiltyCount = jurors.filter((j) => j.currentVote === "not-guilty").length;
  const undecidedCount = jurors.filter((j) => j.currentVote === "undecided").length;

  const guiltyPercentage = (guiltyCount / totalJurors) * 100;
  const notGuiltyPercentage = (notGuiltyCount / totalJurors) * 100;

  return (
    <Card className="p-6 bg-white shadow-lg">
      <h2 className="text-2xl font-crimson mb-4">Current Standing</h2>
      
      <div className="space-y-4">
        <div>
          <div className="flex justify-between mb-2">
            <span className="font-semibold text-burgundy">Guilty</span>
            <span className="text-burgundy">{guiltyCount}/{totalJurors}</span>
          </div>
          <Progress 
            value={guiltyPercentage} 
            className="bg-gray-200 h-2"
          />
        </div>

        <div>
          <div className="flex justify-between mb-2">
            <span className="font-semibold text-navy">Not Guilty</span>
            <span className="text-navy">{notGuiltyCount}/{totalJurors}</span>
          </div>
          <Progress 
            value={notGuiltyPercentage} 
            className="bg-gray-200 h-2"
          />
        </div>

        <div className="mt-4 p-3 bg-gray-50 rounded-lg">
          <p className="text-center text-gray-600">
            {undecidedCount} juror{undecidedCount !== 1 ? "s" : ""} still undecided
          </p>
        </div>
      </div>
    </Card>
  );
};

export default VerdictTracker;