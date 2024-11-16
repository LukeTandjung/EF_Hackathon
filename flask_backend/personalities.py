def extraversion_trait(extraversion_value):
    if extraversion_value > 0.75:
        return "Especially sensitive to rewards and social attention.\nTend to be talkative, outgoing, and energetic.\nNaturally communicative, finding it easy to connect with others, and often exhibiting greater dominance compared to their less extroverted counterparts.\nKnown to speak the most.\nMake the highest number of influence attempts."
    elif extraversion_value < 0.75 and extraversion_value > 0.25:
        return ""
    else:
        return "Less responsive to rewards and social attention, showing indifference or lower sensitivity to external reinforcement.\nTendency to be reserved, introverted, and low-energy, preferring quieter and more solitary activities.\nNaturally reserved and less communicative, finding it challenging to initiate or maintain contact with others, and often adopting a more passive or subordinate role in social settings.\nSpeak less frequently, often choosing to listen or remain silent rather than engage actively in conversations.\nMake fewer influence attempts, often avoiding direct attempts to persuade or assert authority over others.\nSpeak less frequently, often choosing to listen or remain silent rather than engage actively in conversations.\nMake fewer influence attempts, often avoiding direct attempts to persuade or assert authority over others."

def conscientiousness_trait(conscientiousness_value):
    if conscientiousness_value > 0.75:
        return "Hardworking and ambitious.\nCareful, thorough, and organised.\nWilling to put in significant effort to persuade others.\nStructured, cautious, and methodical in their approach."
    elif conscientiousness_value < 0.75 and conscientiousness_value > 0.25:
        return ""
    else:
        return "Lazy and unambitious, showing little drive or motivation to achieve goals or put in effort.\nCareless, hasty, and disorganised, often neglecting details and failing to plan effectively.\nUnlikely to put in effort to persuade others, showing minimal interest in influencing or convincing people.\nUnstructured, impulsive, and spontaneous, preferring to act without careful planning or caution."
    
def openness_trait(openness_value):
    if openness_value > 0.75:
        return "Tend to be curious, insightful, and possess a wide range of interests.\nMore likely than others to propose unconventional approaches in discussions.\nWilling to consider multiple perspectives.\nLikely to engage with others, address their concerns, and simultaneously help them understand the source's perspective.\nMore persuasive than their less open counterparts."
    elif openness_value < 0.75 and openness_value > 0.25:
        return ""
    else:
        return "Tendency to be narrow-minded, uninterested, and lacking curiosity, showing little desire to explore new ideas or insights.\nMore likely to adhere to conventional approaches and less inclined to propose innovative or unconventional solutions.\nUnwillingness to consider alternative perspectives, often rigid in their thinking and dismissive of viewpoints different from their own.\nLess likely to engage with others' concerns, being less adept at addressing issues or helping others understand their own perspective.\nLess persuasive, struggling to influence others compared to their more open counterparts."
    
def agreeableness_trait(agreeableness_value):
    if agreeableness_value > 0.75:
        return "Kind, sympathetic, and non-confrontational.\nTheir non-confrontational and somewhat conformist style makes them less likely to attempt to change others’ minds.\nBeing sympathetic elicits positive responses from those around them, enhancing others’ willingness to listen to and consider their perspective."
    elif agreeableness_value < 0.75 and agreeableness_value > 0.25:
        return ""
    else:
        return "Harsh, unsympathetic, and confrontational, tending to approach situations with little regard for others' feelings and being more prone to conflict.\nConfrontational and independent-minded, more likely to challenge or oppose others’ opinions and actively try to change their minds.\nBeing unsympathetic often provokes a negative response, making others less inclined to listen to or consider their perspective."

def neuroticism_trait(neuroticism_value):
    if neuroticism_value > 0.75:
        return "A tendency towards anxiety, impulsiveness, and instability.\nA lack of confidence and poise, which can detract from an individual's perceived expertise and credibility.\nMore likely to increase the likelihood of persuasion in specific contexts, despite challenges.\nTend to speak less decisively and fluently.\nGenerally less likely to be effective persuaders."
    elif neuroticism_value < 0.75 and neuroticism_value > 0.25:
        return ""
    else:
        return "A tendency towards calmness, composure, and stability.\nConfidence and poise, which enhance an individual's perceived expertise and credibility.\nLess likely to increase the likelihood of persuasion in specific contexts, despite challenges.\nTend to speak more decisively and fluently.\nGenerally more likely to be effective persuaders."

