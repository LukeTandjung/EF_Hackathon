import { useEffect, useRef } from "react";
import { Message, Juror } from "@/types";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

interface DiscussionProps {
  messages: Message[];
  jurors: Juror[];
}

const Discussion = ({ messages, jurors }: DiscussionProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const getJurorById = (id: number) => jurors.find((j) => j.id === id);

  return (
    <Card className="bg-white shadow-lg">
      <div className="p-4 border-b">
        <h2 className="text-2xl font-crimson">Jury Deliberation</h2>
      </div>
      <ScrollArea className="h-[400px] p-4">
        <div className="space-y-4" ref={scrollRef}>
          {messages.map((message) => {
            const juror = getJurorById(message.jurorId);
            return (
              <div
                key={message.id}
                className="animate-fadeIn flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50"
              >
                <span className="text-2xl">{juror?.avatar}</span>
                <div>
                  <div className="flex items-baseline space-x-2">
                    <h3 className="font-crimson font-semibold">{juror?.name}</h3>
                    <span className="text-xs text-gray-500">
                      {message.timestamp.toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-gray-700 mt-1">{message.content}</p>
                </div>
              </div>
            );
          })}
        </div>
      </ScrollArea>
    </Card>
  );
};

export default Discussion;