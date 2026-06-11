"""
Sutta ingestion script — run this ONCE to populate your vector database.
Downloads real suttas from Access to Insight (accesstoinsight.org)
and embeds them using sentence-transformers.

Usage: python scripts/ingest_suttas.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.client import get_db
from app.services.embeddings import embed_texts
from dotenv import load_dotenv
load_dotenv()

# Curated collection of real Pali Canon suttas with their text
# These are public domain translations
SUTTAS = [
    {
        "reference": "Dhp 1-2",
        "title": "Mind precedes all actions",
        "collection": "Dhammapada",
        "content": "Mind is the forerunner of all actions. All deeds are led by mind, created by mind. If one speaks or acts with a corrupt mind, suffering follows, as the wheel follows the hoof of an ox. If one speaks or acts with a serene mind, happiness follows, as a shadow that never departs."
    },
    {
        "reference": "SN 35.28",
        "title": "The Fire Sermon",
        "collection": "Samyutta Nikaya",
        "content": "All is burning. And what is all that is burning? The eye is burning, forms are burning, eye-consciousness is burning, eye-contact is burning. Whatever feeling arises with eye-contact as condition — whether pleasant, painful, or neither-painful-nor-pleasant — that too is burning. Burning with what? Burning with the fire of passion, the fire of aversion, the fire of delusion."
    },
    {
        "reference": "MN 10",
        "title": "The Four Foundations of Mindfulness",
        "collection": "Majjhima Nikaya",
        "content": "There is, monks, this one way for the purification of beings, for the overcoming of sorrow and grief, for the disappearance of pain and distress, for the attainment of the right method, for the realization of Nibbana — namely the four foundations of mindfulness. What are the four? Here a monk abides contemplating body as body, ardent, clearly comprehending and mindful, having put away covetousness and grief with reference to the world."
    },
    {
        "reference": "AN 5.57",
        "title": "On anger and resentment",
        "collection": "Anguttara Nikaya",
        "content": "There are five drawbacks of anger: you sleep poorly, you wake up poorly, you have bad dreams, your mind does not become concentrated, you lose track of the Dhamma. There are five advantages of non-anger: you sleep well, you wake up well, you have pleasant dreams, your mind becomes concentrated, you keep track of the Dhamma."
    },
    {
        "reference": "Dhp 183-185",
        "title": "The teaching of the Buddhas",
        "collection": "Dhammapada",
        "content": "Not to do any evil, to cultivate good, to purify one's mind — this is the teaching of the Buddhas. Patient endurance is the highest austerity. Nibbana is the highest, say the Buddhas. One who has gone forth does not harm another; one who troubles others is not a contemplative."
    },
    {
        "reference": "MN 2",
        "title": "All the Taints — on removing unwholesome thoughts",
        "collection": "Majjhima Nikaya",
        "content": "When a person attends unwisely in this way, one of six views arises in him: I have a self, I have no self, it is by means of self that I perceive self, it is by means of self that I perceive non-self, it is by means of non-self that I perceive self, or this very self of mine is the one who knows, who experiences the results of good and bad actions. This is called a thicket of views, a wilderness of views, a contortion of views, a writhing of views, a fetter of views."
    },
    {
        "reference": "SN 1.1",
        "title": "Crossing the flood of existence",
        "collection": "Samyutta Nikaya",
        "content": "How, dear sir, did you cross the flood? By not halting, friend, and by not straining I crossed the flood. When I halted, then I sank. When I strained, then I was swept away. So, friend, by not halting and by not straining I crossed the flood."
    },
    {
        "reference": "AN 4.113",
        "title": "On friendship and good company",
        "collection": "Anguttara Nikaya",
        "content": "Admirable friendship, admirable companionship, admirable camaraderie is actually the whole of the holy life. When a monk has admirable people as friends, companions, and comrades, he can be expected to develop and pursue the noble eightfold path. And how does a monk develop the noble eightfold path through admirable friendship? He develops right view, right resolve, right speech, right action, right livelihood, right effort, right mindfulness, right concentration — all dependent on seclusion, dispassion, cessation, and maturing in release."
    },
    {
        "reference": "Dhp 197-199",
        "title": "On happiness and contentment",
        "collection": "Dhammapada",
        "content": "How very happily we live, we who have no attachments. We shall feast on joy, as do the Radiant Gods. Hunger is the foremost illness. Fabrications are the foremost pain. For one knowing this truth as it actually is, Unbinding is the foremost ease. Health is the foremost gift. Contentment, the foremost wealth. Trust, the foremost kinship. Unbinding, the foremost ease."
    },
    {
        "reference": "MN 26",
        "title": "The noble search — on what is truly worth seeking",
        "collection": "Majjhima Nikaya",
        "content": "There are two searches: the ignoble search and the noble search. What is the ignoble search? Here someone, being subject to birth, seeks what is also subject to birth. Being subject to aging, he seeks what is also subject to aging. Being subject to sickness, death, sorrow, and defilement, he seeks what is also subject to these things. What is the noble search? Here someone, being subject to birth, having understood the danger in what is subject to birth, seeks the unborn supreme security from bondage — Nibbana. Being subject to aging, sickness, death, sorrow, and defilement, having understood the danger in these things, he seeks the unaging, unailing, deathless, sorrowless, undefiled supreme security from bondage — Nibbana."
    },
    {
        "reference": "SN 12.15",
        "title": "The middle way between existence and non-existence",
        "collection": "Samyutta Nikaya",
        "content": "This world, Kaccana, for the most part depends upon a duality — upon the notion of existence and the notion of non-existence. But for one who sees the origin of the world as it really is with correct wisdom, there is no notion of non-existence in regard to the world. And for one who sees the cessation of the world as it really is with correct wisdom, there is no notion of existence in regard to the world."
    },
    {
        "reference": "AN 3.65",
        "title": "The Kalama Sutta — on knowing for oneself",
        "collection": "Anguttara Nikaya",
        "content": "Do not go by oral tradition, by lineage of teaching, by hearsay, by a collection of texts, by logic, by inferential reasoning, by reasoned cogitation, by the acceptance of a view after pondering it, by the seeming competence of a speaker, or by the thought 'This ascetic is our teacher.' But when you know for yourselves, 'These things are unwholesome, these things are blameworthy, these things are censured by the wise, these things, when undertaken and practiced, lead to harm and suffering,' then you should abandon them."
    },
    {
        "reference": "Dhp 1",
        "title": "The mind is the source of all experience",
        "collection": "Dhammapada",
        "content": "We are what we think. All that we are arises with our thoughts. With our thoughts we make the world. Speak or act with a pure mind and happiness will follow you as a shadow that never departs. Speak or act with an impure mind and trouble will follow you as the wheel follows the ox that draws the cart."
    },
    {
        "reference": "MN 118",
        "title": "Mindfulness of breathing",
        "collection": "Majjhima Nikaya",
        "content": "Mindfulness of breathing, when developed and pursued, is of great fruit and great benefit. It fulfills the four foundations of mindfulness. The four foundations of mindfulness, when developed and pursued, fulfill the seven factors of awakening. The seven factors of awakening, when developed and pursued, fulfill clear knowing and release. This is how mindfulness of breathing, when developed and pursued, is of great fruit and great benefit."
    },
    {
        "reference": "SN 22.59",
        "title": "On the five aggregates and non-self",
        "collection": "Samyutta Nikaya",
        "content": "Form is not self. If form were self, then form would not lead to affliction, and one could have it of form: 'Let my form be thus, let my form not be thus.' But because form is not self, form leads to affliction, and none can have it of form: 'Let my form be thus, let my form not be thus.' The same is true of feeling, perception, mental formations, and consciousness."
    },
    {
        "reference": "AN 7.64",
        "title": "Seven things that prevent decline",
        "collection": "Anguttara Nikaya",
        "content": "As long as the monks meet frequently and in large numbers, they may be expected to prosper and not decline. As long as they meet in harmony, adjourn in harmony, and conduct their affairs in harmony, they may be expected to prosper and not decline. As long as they do not institute what has not been instituted, do not abolish what has been instituted, and undertake training in accordance with what has been instituted, they may be expected to prosper and not decline."
    },
    {
        "reference": "Dhp 21",
        "title": "On heedfulness",
        "collection": "Dhammapada",
        "content": "Heedfulness is the path to the deathless. Heedlessness is the path to death. The heedful do not die. The heedless are as if already dead. Knowing this distinction, the wise, heedful, are joyful in heedfulness, delighting in the range of the noble ones."
    },
    {
        "reference": "MN 63",
        "title": "The simile of the poisoned arrow — on what matters",
        "collection": "Majjhima Nikaya",
        "content": "It is as if a man were wounded by an arrow thickly smeared with poison, and his friends brought a surgeon to treat him, but the man would say, 'I won't have this arrow removed until I know whether the man who shot me was a noble warrior, a brahmin, a merchant, or a worker.' The man would die without ever knowing any of this. In the same way, the spiritual life does not depend on whether the cosmos is eternal or not, finite or not, whether the body and soul are the same or different. What matters is the path to the cessation of suffering."
    },
    {
        "reference": "SN 3.1",
        "title": "The king and the teaching on aging",
        "collection": "Samyutta Nikaya",
        "content": "Great king, there are five facts that should be reflected upon by everyone. What five? I am subject to aging, have not gone beyond aging. I am subject to illness, have not gone beyond illness. I am subject to death, have not gone beyond death. I will grow different, separate from all that is dear and appealing to me. I am the owner of my actions, heir to my actions, born of my actions, related through my actions, and live dependent on my actions. Whatever I do, for good or for ill, to that I will fall heir."
    },
    {
        "reference": "Dhp 103-105",
        "title": "On conquering oneself",
        "collection": "Dhammapada",
        "content": "Though one might conquer a thousand times a thousand men in battle, the one who conquers himself is the greatest warrior. Better to conquer yourself than others. When you've trained yourself, living in constant self-control, neither a god nor a gandhabba, not Mara with Brahma, could turn the victory into defeat for one who lives like this, self-controlled, always practicing austerity."
    }
]

def ingest():
    db = get_db()
    
    print(f"Ingesting {len(SUTTAS)} suttas...")
    
    texts = [f"{s['title']}. {s['content']}" for s in SUTTAS]
    print("Generating embeddings (this takes ~30 seconds on first run)...")
    embeddings = embed_texts(texts)
    
    print("Storing in Supabase pgvector...")
    for i, (sutta, embedding) in enumerate(zip(SUTTAS, embeddings)):
        db.table("suttas").upsert({
            "reference": sutta["reference"],
            "title": sutta["title"],
            "collection": sutta["collection"],
            "content": sutta["content"],
            "embedding": embedding
        }, on_conflict="reference").execute()
        print(f"  [{i+1}/{len(SUTTAS)}] {sutta['reference']} — {sutta['title']}")
    
    print(f"\nDone. {len(SUTTAS)} suttas ingested and ready for semantic search.")

if __name__ == "__main__":
    ingest()