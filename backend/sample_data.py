"""
Sample Data Generator for AI Chat Portal

This script creates sample conversations with realistic messages
for demonstration and testing purposes.

Usage:
    python sample_data.py
"""
import os
import django
import sys
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_portal.settings')
django.setup()

from conversations.models import Conversation, Message
from django.utils import timezone


def create_sample_conversations():
    """Create sample conversations for testing."""
    
    print("Creating sample conversations...")
    
    # Sample Conversation 1: Travel Planning
    conv1 = Conversation.objects.create(
        title="Trip to Japan Planning",
        status="ended",
        start_timestamp=timezone.now() - timedelta(days=7),
        end_timestamp=timezone.now() - timedelta(days=7, hours=-1),
        summary="User discussed planning a trip to Japan for spring, focusing on Tokyo and Kyoto. Key points included booking flights, finding accommodations, and visiting during cherry blossom season.",
        topics=["travel", "Japan", "Tokyo", "Kyoto", "cherry blossoms"],
        key_points=[
            "Book flights by next week",
            "Research hotels in Tokyo and Kyoto",
            "Visit during cherry blossom season (late March - early April)",
            "Budget approximately $3000 for 10-day trip"
        ],
        sentiment="positive"
    )
    
    messages_conv1 = [
        {"sender": "user", "content": "I want to plan a trip to Japan next spring. Can you help me?"},
        {"sender": "ai", "content": "Of course! Japan in spring is beautiful, especially during cherry blossom season. When exactly were you thinking of going, and for how long?"},
        {"sender": "user", "content": "I'm thinking late March or early April for about 10 days. Is that good timing?"},
        {"sender": "ai", "content": "Perfect timing! Late March to early April is peak cherry blossom season. For 10 days, I'd recommend splitting your time between Tokyo (5 days) and Kyoto (4 days), with maybe a day trip. What's your budget looking like?"},
        {"sender": "user", "content": "I'm thinking around $3000 total. Is that realistic?"},
        {"sender": "ai", "content": "Yes, $3000 is reasonable for a 10-day trip if you're mindful of expenses. That covers flights (~$800-1200), accommodation (~$70/night = $700), food (~$40/day = $400), transportation (~$200), and activities (~$500). Would you like me to help you plan the itinerary?"},
        {"sender": "user", "content": "Yes please! What are the must-visit places?"},
        {"sender": "ai", "content": "Great! Here's a suggested itinerary:\n\nTokyo (5 days):\n- Shibuya & Harajuku\n- Senso-ji Temple in Asakusa\n- Tokyo Skytree\n- Tsukiji Outer Market\n- Day trip to Mount Fuji\n\nKyoto (4 days):\n- Fushimi Inari Shrine\n- Arashiyama Bamboo Grove\n- Kinkaku-ji (Golden Pavilion)\n- Gion District\n\nShould I provide more details on any of these?"},
        {"sender": "user", "content": "That sounds amazing! Should I book flights now?"},
        {"sender": "ai", "content": "Yes, I'd recommend booking flights within the next week. Cherry blossom season is very popular, so prices increase closer to the dates. Use flight comparison sites like Google Flights or Skyscanner. Look for flights to Tokyo (Narita or Haneda) and return from Osaka (Kansai) - it's more convenient than backtracking."}
    ]
    
    for i, msg_data in enumerate(messages_conv1):
        Message.objects.create(
            conversation=conv1,
            content=msg_data["content"],
            sender=msg_data["sender"],
            timestamp=conv1.start_timestamp + timedelta(minutes=i*5)
        )
    
    # Sample Conversation 2: Programming Help
    conv2 = Conversation.objects.create(
        title="Learning React Hooks",
        status="ended",
        start_timestamp=timezone.now() - timedelta(days=3),
        end_timestamp=timezone.now() - timedelta(days=3, hours=-0.5),
        summary="User learned about React hooks, specifically useState and useEffect. Discussed practical examples and best practices for managing state and side effects in functional components.",
        topics=["programming", "React", "hooks", "JavaScript", "web development"],
        key_points=[
            "useState for managing component state",
            "useEffect for side effects like API calls",
            "Dependency arrays control when effects run",
            "Custom hooks for reusable logic"
        ],
        sentiment="positive"
    )
    
    messages_conv2 = [
        {"sender": "user", "content": "I'm trying to learn React hooks. Can you explain useState?"},
        {"sender": "ai", "content": "Absolutely! useState is a React hook that lets you add state to functional components. Here's the basic syntax:\n\nconst [count, setCount] = useState(0);\n\n- 'count' is your state variable\n- 'setCount' is the function to update it\n- '0' is the initial value\n\nWould you like to see a practical example?"},
        {"sender": "user", "content": "Yes, please show me an example!"},
        {"sender": "ai", "content": "Here's a simple counter component:\n\nfunction Counter() {\n  const [count, setCount] = useState(0);\n  \n  return (\n    <div>\n      <p>Count: {count}</p>\n      <button onClick={() => setCount(count + 1)}>\n        Increment\n      </button>\n    </div>\n  );\n}\n\nEvery time you click the button, count increases by 1 and the component re-renders with the new value."},
        {"sender": "user", "content": "Cool! What about useEffect?"},
        {"sender": "ai", "content": "useEffect handles side effects in functional components. It runs after every render by default. Common uses:\n- Fetching data from APIs\n- Setting up subscriptions\n- Manually changing the DOM\n\nBasic syntax:\n\nuseEffect(() => {\n  // Your effect code here\n}, [dependencies]);\n\nThe dependency array controls when the effect runs."},
        {"sender": "user", "content": "Can you show me a data fetching example?"},
        {"sender": "ai", "content": "Sure! Here's a component that fetches user data:\n\nfunction UserProfile({ userId }) {\n  const [user, setUser] = useState(null);\n  \n  useEffect(() => {\n    fetch(`/api/users/${userId}`)\n      .then(res => res.json())\n      .then(data => setUser(data));\n  }, [userId]); // Runs when userId changes\n  \n  if (!user) return <div>Loading...</div>;\n  \n  return <div>{user.name}</div>;\n}\n\nThe effect runs when the component mounts and whenever userId changes."}
    ]
    
    for i, msg_data in enumerate(messages_conv2):
        Message.objects.create(
            conversation=conv2,
            content=msg_data["content"],
            sender=msg_data["sender"],
            timestamp=conv2.start_timestamp + timedelta(minutes=i*3)
        )
    
    # Sample Conversation 3: Fitness Advice
    conv3 = Conversation.objects.create(
        title="Starting a Fitness Routine",
        status="ended",
        start_timestamp=timezone.now() - timedelta(days=1),
        end_timestamp=timezone.now() - timedelta(days=1, hours=-0.75),
        summary="User sought advice on starting a fitness routine as a beginner. Discussed workout schedules, proper form, nutrition basics, and the importance of rest days.",
        topics=["fitness", "health", "exercise", "nutrition", "wellness"],
        key_points=[
            "Start with 3 days per week for beginners",
            "Combine cardio and strength training",
            "Proper form is more important than weight",
            "Nutrition: Focus on protein and whole foods",
            "Rest days are crucial for recovery"
        ],
        sentiment="positive"
    )
    
    messages_conv3 = [
        {"sender": "user", "content": "I want to start working out but I'm a complete beginner. Where do I start?"},
        {"sender": "ai", "content": "Great decision! For beginners, I recommend:\n\n1. Start with 3 days/week\n2. Mix cardio (walking, jogging) and basic strength training\n3. Focus on proper form over heavy weights\n4. Begin with 30-45 minute sessions\n\nDo you have access to a gym, or would you prefer home workouts?"},
        {"sender": "user", "content": "I have a gym membership. What exercises should I do?"},
        {"sender": "ai", "content": "Perfect! Here's a beginner-friendly 3-day split:\n\nDay 1 (Upper Body):\n- Push-ups: 3 sets of 10\n- Dumbbell rows: 3 sets of 10\n- Shoulder press: 3 sets of 10\n- Planks: 3 sets of 30 seconds\n\nDay 2 (Lower Body):\n- Squats: 3 sets of 12\n- Lunges: 3 sets of 10 each leg\n- Leg press: 3 sets of 12\n- Calf raises: 3 sets of 15\n\nDay 3 (Full Body + Cardio):\n- 20 minutes moderate cardio\n- Deadlifts: 3 sets of 10\n- Bench press: 3 sets of 10\n- Pull-ups/assisted pull-ups: 3 sets of 5-8\n\nStart with lighter weights to master form!"},
        {"sender": "user", "content": "This is helpful! What about diet?"},
        {"sender": "ai", "content": "Nutrition is 70% of results! Basic guidelines:\n\n1. Protein: 0.7-1g per pound of body weight\n2. Eat whole foods: lean meats, vegetables, fruits, whole grains\n3. Stay hydrated: at least 8 glasses of water daily\n4. Avoid processed foods and excessive sugar\n5. Eat small meals every 3-4 hours\n\nTrack your calories for the first week to understand your intake. Are you trying to lose weight or build muscle?"},
        {"sender": "user", "content": "Mainly lose weight and get toned. Should I work out every day?"},
        {"sender": "ai", "content": "No! Rest days are crucial. Your muscles grow during recovery, not during the workout itself. Stick to 3-4 days per week initially.\n\nFor weight loss:\n- Create a calorie deficit (eat 300-500 calories below maintenance)\n- Combine strength training with cardio\n- Be patient - aim for 1-2 pounds lost per week\n- Track progress with photos and measurements, not just the scale\n\nConsistency over 3-6 months will show real results. You've got this!"}
    ]
    
    for i, msg_data in enumerate(messages_conv3):
        Message.objects.create(
            conversation=conv3,
            content=msg_data["content"],
            sender=msg_data["sender"],
            timestamp=conv3.start_timestamp + timedelta(minutes=i*4)
        )
    
    # Sample Conversation 4: Active conversation
    conv4 = Conversation.objects.create(
        title="Career Advice Discussion",
        status="active",
        start_timestamp=timezone.now() - timedelta(hours=2),
    )
    
    messages_conv4 = [
        {"sender": "user", "content": "I'm thinking about switching careers from marketing to software development. Is it a good idea?"},
        {"sender": "ai", "content": "That's a significant career change! It's definitely possible and many people have made successful transitions into tech. Can you tell me about your current experience with programming?"},
        {"sender": "user", "content": "I've done some online courses in Python and JavaScript. I enjoy it but I'm not sure if I'm good enough to make it a career."},
        {"sender": "ai", "content": "Imposter syndrome is very common in career transitions! The fact that you've already started learning is great. Here's what I'd recommend:\n\n1. Build a portfolio of 3-5 projects\n2. Contribute to open-source\n3. Network with developers\n4. Consider a coding bootcamp for structure\n5. Start applying for junior positions\n\nYour marketing background is actually valuable - developer relations, technical writing, and product management value that skillset. Have you thought about which area of software development interests you most?"}
    ]
    
    for i, msg_data in enumerate(messages_conv4):
        Message.objects.create(
            conversation=conv4,
            content=msg_data["content"],
            sender=msg_data["sender"],
            timestamp=conv4.start_timestamp + timedelta(minutes=i*5)
        )
    
    print(f"✅ Successfully created {Conversation.objects.count()} conversations")
    print(f"✅ Successfully created {Message.objects.count()} messages")
    print("\nSample conversations:")
    for conv in Conversation.objects.all():
        print(f"  - {conv.title} ({conv.status}) - {conv.get_message_count()} messages")


def clear_existing_data():
    """Clear all existing conversations and messages."""
    Message.objects.all().delete()
    Conversation.objects.all().delete()
    print("🗑️  Cleared all existing data")


if __name__ == "__main__":
    print("=" * 60)
    print("AI Chat Portal - Sample Data Generator")
    print("=" * 60)
    print()
    
    response = input("This will clear existing data. Continue? (yes/no): ")
    if response.lower() == 'yes':
        clear_existing_data()
        create_sample_conversations()
        print("\n" + "=" * 60)
        print("Sample data creation complete!")
        print("=" * 60)
    else:
        print("Operation cancelled.")

