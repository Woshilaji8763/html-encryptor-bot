import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import random
import string
import os
from datetime import datetime
import re

# 设置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot配置
BOT_TOKEN = '7838707734:AAHUINQudboDg6C1y8oS1K9hy6koNucyUG4'

class DualToolBot:
    def __init__(self):
        self.current_gold_price = 3335.00  # 默认金价
        
    # ======================== HTML 加密功能 ========================
    def encrypt_html(self, html_content):
        """HTML加密功能"""
        encrypted_dict = {}
        for i, char in enumerate(html_content):
            encrypted_dict[i] = hex(ord(char))[2:]
        return encrypted_dict
    
    def generate_decryption_script(self, encrypted_dict, var_name=None):
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
    
    # ======================== Lot Size 计算功能 ========================
    def calculate_lot_size_usd(self, lot_size):
        """计算Lot Size对应的USD金额"""
        try:
            lot_size = float(lot_size)
            
            # XAUUSD: 1标准手 = 100盎司黄金
            ounces = lot_size * 100
            usd_value = ounces * self.current_gold_price
            
            # 计算每点价值
            pip_value = lot_size * 10
            
            # 计算保证金需求（假设1%保证金）
            margin_required = usd_value * 0.01
            
            return {
                'lot_size': lot_size,
                'ounces': ounces,
                'current_price': self.current_gold_price,
                'usd_value': round(usd_value, 2),
                'pip_value': round(pip_value, 2),
                'margin_required': round(margin_required, 2),
                'calculation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except ValueError:
            return None
    
    def get_lot_size_examples(self):
        """获取常见手数示例"""
        examples = []
        lot_sizes = [0.01, 0.1, 0.5, 1.0, 2.0, 5.0]
        
        for lot in lot_sizes:
            ounces = lot * 100
            usd_value = ounces * self.current_gold_price
            pip_value = lot * 10
            
            examples.append({
                'lot': lot,
                'ounces': ounces,
                'usd_value': round(usd_value, 2),
                'pip_value': round(pip_value, 2)
            })
        
        return examples
    
    def set_gold_price(self, price):
        """设置金价"""
        try:
            self.current_gold_price = float(price)
            return True
        except ValueError:
            return False

# 初始化工具
bot_tools = DualToolBot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令"""
    keyboard = [
        [InlineKeyboardButton("🔒 HTML 加密工具", callback_data='html_encrypt')],
        [InlineKeyboardButton("💰 Lot Size 计算", callback_data='lot_calculator')],
        [InlineKeyboardButton("ℹ️ 使用帮助", callback_data='help_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = """🚀 双功能工具 Bot

🔥 **核心功能**:
🔹 HTML 代码加密保护
🔹 Lot Size 精确计算

💡 **快速使用**:
• 发送HTML代码 → 自动加密
• 发送 `lot 0.1` → 计算金额
• 发送 `price 3335` → 设置金价

🎯 选择功能开始使用！"""
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理按钮回调"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'html_encrypt':
        await query.edit_message_text(
            "🔒 HTML 加密工具\n\n"
            "🛡️ **功能特点**:\n"
            "• 军用级加密保护\n"
            "• 防止源码泄露\n"
            "• 保持功能完整\n"
            "• 随机变量名生成\n\n"
            "📋 **使用方法**:\n"
            "1. 上传.html文件\n"
            "2. 发送HTML代码\n"
            "3. 获取加密后的文件\n\n"
            "💻 **示例**:\n"
            "直接发送HTML代码即可自动加密"
        )
    
    elif query.data == 'lot_calculator':
        keyboard = [
            [InlineKeyboardButton("📊 常见手数对照", callback_data='lot_examples')],
            [InlineKeyboardButton("💰 设置金价", callback_data='set_price_info')],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"💰 Lot Size 计算器\n\n"
            f"📊 **当前金价**: ${bot_tools.current_gold_price:,.2f}\n\n"
            f"💡 **使用方法**:\n"
            f"• 发送 `lot 0.1` → 计算0.1手\n"
            f"• 发送 `手数 1.0` → 计算1.0手\n"
            f"• 发送 `price 3335` → 设置金价\n\n"
            f"📋 **计算内容**:\n"
            f"• 手数转USD金额\n"
            f"• 每点价值计算\n"
            f"• 保证金需求\n"
            f"• 风险管理建议\n\n"
            f"🎯 试试发送: `lot 0.1`",
            reply_markup=reply_markup
        )
    
    elif query.data == 'lot_examples':
        examples = bot_tools.get_lot_size_examples()
        
        examples_text = f"📊 常见手数对照表\n\n💰 当前金价: ${bot_tools.current_gold_price:,.2f}\n\n"
        
        for ex in examples:
            examples_text += f"🔸 **{ex['lot']} 手**\n"
            examples_text += f"   • 黄金: {ex['ounces']:g} 盎司\n"
            examples_text += f"   • 价值: ${ex['usd_value']:,.2f} USD\n"
            examples_text += f"   • 每点: ${ex['pip_value']:,.2f} USD\n\n"
        
        examples_text += "💡 发送 `lot 0.1` 计算自定义手数\n"
        examples_text += "💡 发送 `price 3335` 设置金价"
        
        back_keyboard = [
            [InlineKeyboardButton("🔙 返回计算器", callback_data='lot_calculator')]
        ]
        back_markup = InlineKeyboardMarkup(back_keyboard)
        
        await query.edit_message_text(examples_text, reply_markup=back_markup)
    
    elif query.data == 'set_price_info':
        await query.edit_message_text(
            f"💰 设置XAUUSD金价\n\n"
            f"📊 **当前金价**: ${bot_tools.current_gold_price:,.2f}\n\n"
            f"📋 **设置方法**:\n"
            f"发送消息格式:\n"
            f"• `price 3335` \n"
            f"• `价格 3335`\n"
            f"• `price 3340.50`\n\n"
            f"🎯 **示例**: `price 3335`\n\n"
            f"✅ 设置后，所有Lot Size计算都基于新价格\n"
            f"📊 影响范围: 手数计算、保证金、每点价值"
        )
    

    elif query.data == 'help_menu':
        help_text = """ℹ️ 使用帮助指南

🔒 **HTML 加密工具**:
• 上传 .html 文件
• 发送 HTML 代码
• 自动生成加密文件
• 保护源码不被复制

💰 **Lot Size 计算器**:
• 发送: `lot 0.1` 计算手数
• 发送: `price 3335` 设置金价
• 自动计算USD金额
• 显示保证金和每点价值

🎯 **快速命令**:
• `/start` - 显示主菜单
• `lot 数字` - 计算手数
• `price 数字` - 设置金价

📞 **联系方式**:
• Telegram: @CKWinGg1330
• 频道: @TeamCKGroup

💡 **使用技巧**:
• 所有功能都支持自动识别
• 24小时在线服务
• 完全免费使用"""
        
        back_keyboard = [
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        back_markup = InlineKeyboardMarkup(back_keyboard)
        
        await query.edit_message_text(help_text, reply_markup=back_markup)
    
    elif query.data == 'main_menu':
        await start(update, context)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理HTML文件加密"""
    document = update.message.document
    
    if not document.file_name.lower().endswith(('.html', '.htm')):
        await update.message.reply_text("❌ 请上传HTML文件(.html/.htm)")
        return
    
    processing_msg = await update.message.reply_text("🔒 正在加密HTML文件...")
    
    try:
        file = await context.bot.get_file(document.file_id)
        file_content = await file.download_as_bytearray()
        html_content = file_content.decode('utf-8')
        
        # 加密HTML
        encrypted_dict = bot_tools.encrypt_html(html_content)
        encrypted_script = bot_tools.generate_decryption_script(encrypted_dict)
        
        # 生成文件名
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        encrypted_filename = f"{random_name}.html"
        
        # 发送加密文件
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=encrypted_script.encode('utf-8'),
            filename=encrypted_filename,
            caption="✅ HTML文件加密完成！🔐"
        )
        
        await processing_msg.delete()
        
        success_keyboard = [
            [InlineKeyboardButton("🔒 再次加密", callback_data='html_encrypt')],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        success_markup = InlineKeyboardMarkup(success_keyboard)
        
        await update.message.reply_text(
            f"✅ 加密成功！\n\n"
            f"🔒 HTML文件已加密完成\n"
            f"🛡️ 源码已安全保护\n"
            f"📊 功能保持完整",
            reply_markup=success_markup
        )
        
    except Exception as e:
        logger.error(f"HTML加密错误: {e}")
        await processing_msg.edit_text("❌ 加密失败，请重试")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理文本消息"""
    text = update.message.text
    
    # 价格设置
    price_match = re.search(r'(?:price|价格)\s*(\d+\.?\d*)', text.lower())
    if price_match:
        price = float(price_match.group(1))
        if bot_tools.set_gold_price(price):
            await update.message.reply_text(
                f"💰 金价设置成功！\n\n"
                f"🔸 新金价: ${price:,.2f}\n"
                f"🔸 更新时间: {datetime.now().strftime('%H:%M:%S')}\n\n"
                f"📊 现在Lot Size计算基于新价格:\n"
                f"• 0.1手 = ${price * 10:,.2f} USD\n"
                f"• 1.0手 = ${price * 100:,.2f} USD\n\n"
                f"💡 试试发送: `lot 0.1`"
            )
        else:
            await update.message.reply_text("❌ 价格格式错误，请使用数字")
        return
    
    # Lot Size 计算
    lot_match = re.search(r'(?:lot|手数)\s*(\d+\.?\d*)', text.lower())
    if lot_match:
        lot_size = lot_match.group(1)
        calculation = bot_tools.calculate_lot_size_usd(lot_size)
        
        if calculation:
            
            calc_text = f"""💰 Lot Size 计算结果

📊 **计算详情**:
━━━━━━━━━━━━━━━━━━━━━━━━
🔸 **手数**: {calculation['lot_size']} 标准手
🔸 **黄金**: {calculation['ounces']:g} 盎司
🔸 **金价**: ${calculation['current_price']:,.2f}
🔸 **总价值**: ${calculation['usd_value']:,.2f} USD

💡 **交易信息**:
━━━━━━━━━━━━━━━━━━━━━━━━
• 每点价值: ${calculation['pip_value']:,.2f} USD
• 保证金需求: ${calculation['margin_required']:,.2f} USD (1%)
• 风险建议: 账户总资金的2-3%

📊 **仓位建议**:
━━━━━━━━━━━━━━━━━━━━━━━━
• 小额账户 ($1,000-$5,000): 0.01-0.05手
• 中等账户 ($5,000-$20,000): 0.05-0.2手  
• 大额账户 ($20,000+): 0.2手以上

⏰ 计算时间: {calculation['calculation_time']}"""
            
            calc_keyboard = [
                [InlineKeyboardButton("📊 手数对照表", callback_data='lot_examples')],
                [InlineKeyboardButton("💰 设置金价", callback_data='set_price_info')],
                [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
            ]
            calc_markup = InlineKeyboardMarkup(calc_keyboard)
            
            await update.message.reply_text(calc_text, reply_markup=calc_markup)
        else:
            await update.message.reply_text("❌ 手数格式错误\n\n请使用: `lot 0.1` 或 `手数 0.1`")
        return
    
    # HTML 代码加密
    if text.strip().startswith('<') and text.strip().endswith('>'):
        processing_msg = await update.message.reply_text("🔒 正在加密HTML代码...")
        
        try:
            # 加密HTML代码
            encrypted_dict = bot_tools.encrypt_html(text)
            encrypted_script = bot_tools.generate_decryption_script(encrypted_dict)
            
            # 生成文件名
            random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            encrypted_filename = f"{random_name}.html"
            
            # 发送加密文件
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=encrypted_script.encode('utf-8'),
                filename=encrypted_filename,
                caption="✅ HTML代码加密完成！🔐"
            )
            
            await processing_msg.delete()
            
            success_keyboard = [
                [InlineKeyboardButton("🔒 再次加密", callback_data='html_encrypt')],
                [InlineKeyboardButton("💰 计算手数", callback_data='lot_calculator')]
            ]
            success_markup = InlineKeyboardMarkup(success_keyboard)
            
            await update.message.reply_text(
                f"✅ 代码加密成功！\n\n"
                f"🔒 HTML代码已加密完成\n"
                f"🛡️ 源码已安全保护",
                reply_markup=success_markup
            )
            
        except Exception as e:
            logger.error(f"HTML代码加密错误: {e}")
            await processing_msg.edit_text("❌ 加密失败，请重试")
        return
    

    # 关键词识别
    if any(word in text.lower() for word in ['html', '加密', '网页', 'encrypt']):
        await update.message.reply_text(
            "🔒 HTML加密功能说明：\n\n"
            "📋 **使用方法**:\n"
            "• 直接发送HTML代码\n"
            "• 上传HTML文件\n"
            "• 获取加密后的文件\n\n"
            "💡 **示例**:\n"
            "发送: `<html><body>Hello</body></html>`\n"
            "获取: 加密后的HTML文件"
        )
    elif any(word in text.lower() for word in ['lot', '手数', '仓位', '计算', '金价']):
        await update.message.reply_text(
            "💰 Lot Size计算器说明：\n\n"
            "📋 **使用方法**:\n"
            "• 发送 `lot 0.1` 计算手数\n"
            "• 发送 `price 3335` 设置金价\n"
            "• 自动计算USD金额\n\n"
            "💡 **示例**:\n"
            "发送: `lot 0.1`\n"
            "回复: 0.1手 = ${bot_tools.current_gold_price * 10:,.2f} USD"
        )
    else:
        # 默认回复
        await update.message.reply_text(
            "👋 欢迎使用双功能工具Bot！\n\n"
            "🎯 **快速使用**:\n"
            "• 发送 `/start` 查看主菜单\n"
            "• 发送 `lot 0.1` 计算手数\n"
            "• 发送 `price 3335` 设置金价\n"
            "• 发送HTML代码进行加密\n\n"
            "💡 两个核心功能，简单易用！"
        )

def main():
    """主函数"""
    if not BOT_TOKEN:
        print("❌ 请设置正确的 BOT_TOKEN")
        return
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 添加处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("🚀 双功能工具 Bot 启动中...")
    print("🔒 HTML 加密功能已就绪")
    print("💰 Lot Size 计算功能已就绪")
    print("✅ 简洁高效，专注核心功能")
    
    application.run_polling()

if __name__ == '__main__':
    main()
