import telebot
import google.generativeai as genai

# 1. ضع هنا التوكن الخاص ببوت تليجرام
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# 2. ضع هنا مفتاح Gemini API
GEMINI_KEY = 'YOUR_GEMINI_API_KEY'

# إعداد الذكاء الاصطناعي
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# رسالة الترحيب
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت تلخيص منهج أولى ثانوي! 📚\nابعتلي أي نص أو درس، وهعملك ملخص (س وج) ونقاط هامة.")

# استقبال النصوص وتلخيصها
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    
    # رسالة انتظار للمستخدم
    wait_msg = bot.reply_to(message, "جاري قراءة الدرس وتلخيصه... انتظر ثانية ⏳")
    
    try:
        # البرومبت (الأمر) اللي بيخلي الذكاء الاصطناعي يركز على أولى ثانوي
        prompt = f"أنت مدرس خبير في المنهج المصري لأولى ثانوي. لخص النص التالي بأسلوب منظم (نقاط هامة، تعريفات، 3 أسئلة متوقعة): \n\n {user_input}"
        
        response = model.generate_content(prompt)
        
        # إرسال التلخيص
        bot.edit_message_text(response.text, chat_id=message.chat.id, message_id=wait_msg.message_id)
        
    except Exception as e:
        bot.edit_message_text("عذراً، حدث خطأ ما. حاول مرة أخرى لاحقاً.", chat_id=message.chat.id, message_id=wait_msg.message_id)

print("البوت يعمل الآن...")
bot.polling()
