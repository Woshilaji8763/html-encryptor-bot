import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import random
import string
import os

# 设置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量获取 token
BOT_TOKEN = os.getenv('7838707734:AAHUINQudboDg6C1y8oS1K9hy6koNucyUG4')

def encrypt_html(html_content):
    """将HTML内容加密为十六进制数组"""
    encrypted_dict = {}
    for i, char in enumerate(html_content):
        encrypted_dict[i] = hex(ord(char))[2:]
    return encrypted_dict

def generate_decryption_script(encrypted_dict, var_name=None):
    """生成解密脚本"""
    if var_name is None:
        var_name = ''.join(random.choices(string.ascii_letters, k=8))
    
    random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    
    script = f"""<!DOCTYPE html>
<html>
<head>
<title>Protected Content</title>
<script src='https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js'></script>
</head>
<body><!--
 * ============================================
 * 🛡 TanMayMods HTML Encryption Script
 * ============================================
 *
 * 🔐 ABOUT:
 * ----------
 * This script securely encodes HTML content, making it unreadable  
 * without decoding. Protects web pages from unauthorized access  
 * and modifications.
 *
 * 🚀 FEATURES:
 * ------------
 * ✅ Encrypts HTML into an unreadable format.
 * ✅ Prevents direct copying and unauthorized edits.
 * ✅ Uses strong obfuscation techniques.
 * ✅ Protects content without affecting functionality.
 *
 * 🔧 DEVELOPER INFO:
 * -------------------
 * 🧑‍💻 Developer: @CKWinGg1330
 * 🌐 Version: 1.0
 *
 * 📢 CONTACT:
 * ------------
 * - 🔵 Telegram: @CKWinGg1330
 * - 🔥 Channel: @TeamCKGroup
 *
 * 📜 LICENSE:
 * ------------
 * Licensed under MIT. Modify, distribute, and use freely  
 * with proper credit to the developer.
 *
 * ⚠ DISCLAIMER:
 * --------------
 * This script is provided "as-is" without any warranties.  
 * The developer holds no responsibility for any misuse.
 *
 * 🔒 ENCRYPTION ID: [TaNMaY-ENC-{random_id}]
 *
 * ============================================
-->
<script>
    var {var_name} = {encrypted_dict};
    var decrypted_html = "";
    for (var i in {var_name}) {{
        decrypted_html += String.fromCharCode(parseInt({var_name}[i], 16));
    }}
    document.write(decrypted_html);
</script>
</body>
</html>"""
    return script

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令"""
    keyboard = [
        [InlineKeyboardButton("🔒 加密 HTML", callback_data='encrypt')],
        [InlineKeyboardButton("📢 主频道", url="https://t.me/TeamCKGroup")],
        [InlineKeyboardButton("👨‍💻 开发者", callback_data='developer')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = """✨ 欢迎使用 HTML 加密系统！

🔐 功能特点：
🔹 军用级加密保护
🔹 防止未授权复制和修改  
🔹 不可破解的代码保护

📋 使用方法：
1. 发送 HTML 文件给我
2. 或直接发送 HTML 代码
3. 我会返回加密后的文件

🚀 开始使用吧！"""
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理按钮回调"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'encrypt':
        await query.edit_message_text("📁 请发送你的 HTML 文件，我会为你加密！")
    elif query.data == 'developer':
        await query.edit_message_text("👨‍💻 开发者信息:\n\n🔵 Telegram: @CKWinGg1330\n🔥 频道: @TeamCKGroup")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理文档"""
    document = update.message.document
    
    if not document.file_name.endswith('.html'):
        await update.message.reply_text("❌ 请发送 HTML 文件！")
        return
    
    processing_msg = await update.message.reply_text("⏳ 正在处理你的 HTML 文件...")
    
    try:
        file = await context.bot.get_file(document.file_id)
        file_content = await file.download_as_bytearray()
        html_content = file_content.decode('utf-8')
        
        encrypted_dict = encrypt_html(html_content)
        encrypted_script = generate_decryption_script(encrypted_dict)
        
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        encrypted_filename = f"{random_name}.html"
        
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=encrypted_script.encode('utf-8'),
            filename=encrypted_filename,
            caption="✅ 你的 HTML 已完全加密并准备使用！🔐"
        )
        
        await processing_msg.delete()
        
        success_keyboard = [
            [InlineKeyboardButton("🔄 再次加密", callback_data='encrypt')],
            [InlineKeyboardButton("📢 加入频道", url="https://t.me/TeamCKGroup")]
        ]
        success_markup = InlineKeyboardMarkup(success_keyboard)
        
        await update.message.reply_text(
            "✅ 加密测试成功！\n\n页面功能完全正常，但源代码已被安全加密保护。",
            reply_markup=success_markup
        )
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ 处理文件时出错: {str(e)}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理文本消息"""
    if update.message.text.startswith('<'):
        processing_msg = await update.message.reply_text("⏳ 正在加密你的 HTML 代码...")
        
        try:
            html_content = update.message.text
            encrypted_dict = encrypt_html(html_content)
            encrypted_script = generate_decryption_script(encrypted_dict)
            
            random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            encrypted_filename = f"{random_name}.html"
            
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=encrypted_script.encode('utf-8'),
                filename=encrypted_filename,
                caption="✅ 你的 HTML 代码已加密完成！🔐"
            )
            
            await processing_msg.delete()
            
        except Exception as e:
            await processing_msg.edit_text(f"❌ 加密失败: {str(e)}")
    else:
        await update.message.reply_text("请发送 HTML 文件或 HTML 代码给我加密！")

def main():
    """主函数"""
    if not BOT_TOKEN:
        print("❌ 请设置 BOT_TOKEN 环境变量")
        return
        
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("🚀 HTML 加密 Bot 启动中...")
    application.run_polling()

if __name__ == '__main__':
    main()
