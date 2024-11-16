export interface Juror {
  id: number;
  name: string;
  personality: {
    openness: number;
    conscientiousness: number;
    extraversion: number;
    agreeableness: number;
    neuroticism: number;
  };
  avatar: string;
  currentVote: "guilty" | "not-guilty" | "undecided";
  gender: string;
  race: string;
  politicalBelief: string;
  religion: string;
}

export interface Message {
  id: number;
  jurorId: number;
  content: string;
  timestamp: Date;
}

export interface Case {
  title: string;
  description: string;
  prosecution: string;
  defense: string;
}