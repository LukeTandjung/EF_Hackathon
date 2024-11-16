import { Juror } from "@/types";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface JuryPanelProps {
  jurors: Juror[];
}

const JuryPanel = ({ jurors }: JuryPanelProps) => {
  const getVoteBadgeColor = (vote: string) => {
    switch (vote) {
      case "guilty":
        return "bg-burgundy text-white";
      case "not-guilty":
        return "bg-navy text-white";
      default:
        return "bg-gray-200 text-gray-700";
    }
  };

  const formatPersonality = (personality: Juror['personality']) => {
    const highestTrait = Object.entries(personality)
      .reduce((a, b) => a[1] > b[1] ? a : b);
    return `High ${highestTrait[0]}`;
  };

  return (
    <Card className="p-6 bg-white shadow-lg">
      <h2 className="text-2xl font-crimson mb-4">Jury Panel</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {jurors.map((juror) => (
          <div
            key={juror.id}
            className="p-4 border rounded-lg hover:shadow-md transition-shadow"
          >
            <div className="flex items-center space-x-3">
              <span className="text-3xl">{juror.avatar}</span>
              <div>
                <h3 className="font-crimson font-semibold">{juror.name}</h3>
                <p className="text-sm text-gray-600">{formatPersonality(juror.personality)}</p>
              </div>
            </div>
            <Badge className={`mt-2 ${getVoteBadgeColor(juror.currentVote)}`}>
              {juror.currentVote.replace("-", " ")}
            </Badge>
          </div>
        ))}
      </div>
    </Card>
  );
};

export default JuryPanel;