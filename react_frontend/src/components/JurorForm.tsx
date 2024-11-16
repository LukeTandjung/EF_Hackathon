import { Juror } from "@/types";
import { Input } from "@/components/ui/input";
import { Slider } from "@/components/ui/slider";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface JurorFormProps {
  juror: Juror;
  index: number;
  onChange: (updates: Partial<Juror>) => void;
}

export const JurorForm = ({ juror, index, onChange }: JurorFormProps) => {
  return (
    <div key={juror.id} className="mb-8 p-4 border rounded-lg">
      <h3 className="text-lg font-semibold mb-4">Juror {index + 1}</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm mb-1">Name</label>
          <Input
            value={juror.name}
            onChange={(e) => onChange({ name: e.target.value })}
          />
        </div>

        <div>
          <label className="block text-sm mb-1">Gender</label>
          <Select
            value={juror.gender}
            onValueChange={(value) => onChange({ gender: value })}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select gender" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="Male">Male</SelectItem>
              <SelectItem value="Female">Female</SelectItem>
              <SelectItem value="Non-binary">Non-binary</SelectItem>
              <SelectItem value="Prefer not to say">Prefer not to say</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div>
          <label className="block text-sm mb-1">Race/Ethnicity</label>
          <Select
            value={juror.race}
            onValueChange={(value) => onChange({ race: value })}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select race/ethnicity" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="Asian">Asian</SelectItem>
              <SelectItem value="Black">Black</SelectItem>
              <SelectItem value="Hispanic">Hispanic</SelectItem>
              <SelectItem value="White">White</SelectItem>
              <SelectItem value="Other">Other</SelectItem>
              <SelectItem value="Prefer not to say">Prefer not to say</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div>
          <label className="block text-sm mb-1">Political Belief</label>
          <Select
            value={juror.politicalBelief}
            onValueChange={(value) => onChange({ politicalBelief: value })}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select political belief" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="Conservative">Conservative</SelectItem>
              <SelectItem value="Liberal">Liberal</SelectItem>
              <SelectItem value="Moderate">Moderate</SelectItem>
              <SelectItem value="Independent">Independent</SelectItem>
              <SelectItem value="Other">Other</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div>
          <label className="block text-sm mb-1">Religion</label>
          <Select
            value={juror.religion}
            onValueChange={(value) => onChange({ religion: value })}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select religion" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="Christianity">Christianity</SelectItem>
              <SelectItem value="Islam">Islam</SelectItem>
              <SelectItem value="Judaism">Judaism</SelectItem>
              <SelectItem value="Buddhism">Buddhism</SelectItem>
              <SelectItem value="Hinduism">Hinduism</SelectItem>
              <SelectItem value="None">None</SelectItem>
              <SelectItem value="Other">Other</SelectItem>
              <SelectItem value="Prefer not to say">Prefer not to say</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="space-y-4">
        <h4 className="font-medium">Personality Traits (Big Five)</h4>
        
        {Object.entries(juror.personality).map(([trait, value]) => (
          <div key={trait}>
            <label className="block text-sm mb-1 capitalize">{trait}</label>
            <Slider
              value={[value]}
              min={0}
              max={100}
              step={1}
              onValueChange={([newValue]) => 
                onChange({
                  personality: { ...juror.personality, [trait]: newValue }
                })
              }
            />
          </div>
        ))}
      </div>
    </div>
  );
};