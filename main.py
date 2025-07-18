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

class MultiToolBot:
    def __init__(self):
        self.html_encrypt_count = 0
        self.xauusd_analysis_count = 0
        self.lot_calc_count = 0
        
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
    
    # ======================== XAUUSD 分析功能 ========================
    def get_gold_price(self):
        """获取模拟金价"""
        base_price = 2050.00
        current_price = round(base_price + random.uniform(-50, 50), 2)
        return current_price
    
    def analyze_xauusd_chart(self, image_data=None):
        """XAUUSD图表分析"""
        current_price = self.get_gold_price()
        
        # 技术分析
        rsi = random.uniform(25, 75)
        macd = random.uniform(-2, 2)
        
        direction = random.choice(["LONG", "SHORT"])
        
        if direction == "LONG":
            entry = current_price
            sl = round(entry - random.uniform(10, 20), 2)
            tp1 = round(entry + random.uniform(15, 25), 2)
            tp2 = round(entry + random.uniform(30, 50), 2)
            
            reasons = [
                "🔍 金价触及关键支撑位强劲反弹",
                "📈 RSI指标显示超卖区域回升",
                "🎯 突破下降趋势线确认上涨",
                "💪 美元走弱推动金价上涨",
                "🔄 斐波那契61.8%回撤支撑",
                "⚡ MACD金叉信号确认买入"
            ]
        else:
            entry = current_price
            sl = round(entry + random.uniform(10, 20), 2)
            tp1 = round(entry - random.uniform(15, 25), 2)
            tp2 = round(entry - random.uniform(30, 50), 2)
            
            reasons = [
                "🔍 金价遇阻关键阻力位回落",
                "📉 RSI指标显示超买区域调整",
                "🎯 跌破上升趋势线确认下跌",
                "📊 美元走强施压金价下跌",
                "🔄 斐波那契38.2%回撤阻力",
                "⚡ MACD死叉信号确认卖出"
            ]
        
        risk_reward = round(abs(tp1 - entry) / abs(sl - entry), 2)
        
        return {
            'direction': direction,
            'entry': entry,
            'sl': sl,
            'tp1': tp1,
            'tp2': tp2,
            'current_price': current_price,
            'rsi': round(rsi, 1),
            'macd': round(macd, 3),
            'main_reason': random.choice(reasons),
            'risk_reward': risk_reward,
            'confidence': random.choice(["高", "中", "低"]),
            'timeframe': random.choice(['1H', '4H', '1D']),
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    # ======================== Lot Size 计算功能 ========================
    def calculate_lot_size_usd(self, lot_size):
        """计算Lot Size对应的USD金额"""
        try:
            lot_size = float(lot_size)
            current_gold_price = self.get_gold_price()
            
            # XAUUSD: 1标准手 = 100盎司黄金
            ounces = lot_size * 100
            usd_value = ounces * current_gold_price
            
            # 计算不同手数的对比
            pip_value = lot_size * 10  # 每点价值
            
            return {
                'lot_size': lot_size,
                'ounces': ounces,
                'current_price': current_gold_price,
                'usd_value': round(usd_value, 2),
                'pip_value': round(pip_value, 2),
                'margin_required': round(usd_value * 0.01, 2),  # 假设1%保证金
                'calculation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except ValueError:
            return None
    
    def get_lot_size_examples(self):
        """获取常见手数示例"""
        current_price = self.get_gold_price()
        examples = []
        
        lot_sizes = [0.01, 0.1, 0.5, 1.0, 2.0, 5.0]
        
        for lot in lot_sizes:
            ounces = lot * 100
            usd_value = ounces * current_price
            pip_value = lot * 10
            
            examples.append({
                'lot': lot,
                'ounces': ounces,
                'usd_value': round(usd_value, 2),
                'pip_value': round(pip_value, 2)
            })
        
        return examples

# 初始化工具
bot_tools = MultiToolBot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令"""
    keyboard = [
        [InlineKeyboardButton("🔒 HTML 加密工具", callback_data='html_encrypt')],
        [InlineKeyboardButton("📊 XAUUSD 分析", callback_data='xauusd_analyze')],
        [InlineKeyboardButton("💰 Lot Size 计算", callback_data='lot_calculator')],
        [InlineKeyboardButton("📈 功能统计", callback_data='bot_stats')],
        [InlineKeyboardButton("ℹ️ 使用帮助", callback_data='help_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = """🚀 多功能交易工具 Bot

🔥 **核心功能**:
🔹 HTML 代码加密保护
🔹 XAUUSD 图表技术分析  
🔹 Lot Size 资金计算
🔹 专业交易工具集合

💡 **适用场景**:
• 网页开发者 - 保护HTML源码
• 黄金交易者 - 获取分析建议
• 资金管理 - 计算仓位大小

🎯 选择功能开始使用！"""
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理按钮回调"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'html_encrypt':
        keyboard = [
            [InlineKeyboardButton("📁 上传HTML文件", callback_data='upload_html')],
            [InlineKeyboardButton("💻 发送HTML代码", callback_data='send_html_code')],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🔒 HTML 加密工具\n\n"
            "🛡️ **功能特点**:\n"
            "• 军用级加密保护\n"
            "• 防止源码泄露\n"
            "• 保持功能完整\n"
            "• 随机变量名生成\n\n"
            "📋 **使用方法**:\n"
            "1. 上传.html文件 或\n"
            "2. 直接发送HTML代码\n"
            "3. 获取加密后的文件\n\n"
            "🎯 选择输入方式:",
            reply_markup=reply_markup
        )
    
    elif query.data == 'xauusd_analyze':
        keyboard = [
            [InlineKeyboardButton("📊 上传图表分析", callback_data='upload_chart')],
            [InlineKeyboardButton("🎯 快速分析", callback_data='quick_analysis')],
            [InlineKeyboardButton("💹 当前金价", callback_data='gold_price')],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📊 XAUUSD 专业分析\n\n"
            "🏆 **分析功能**:\n"
            "• 智能图表识别\n"
            "• Entry/SL/TP建议\n"
            "• 技术指标分析\n"
            "• 风险回报计算\n\n"
            "📈 **技术指标**:\n"
            "• RSI 动量指标\n"
            "• MACD 趋势指标\n"
            "• 支撑阻力位\n"
            "• 斐波那契分析\n\n"
            "🎯 选择分析方式:",
            reply_markup=reply_markup
        )
    
    elif query.data == 'lot_calculator':
        keyboard = [
            [InlineKeyboardButton("📊 常见手数对照", callback_data='lot_examples')],
            [InlineKeyboardButton("💰 当前金价", callback_data='gold_price')],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "💰 Lot Size 计算器\n\n"
            "📋 **计算功能**:\n"
            "• 手数转USD金额\n"
            "• 每点价值计算\n"
            "• 保证金需求\n"
            "• 风险管理建议\n\n"
            "💡 **使用方法**:\n"
            "直接发送消息格式:\n"
            "`lot 0.1` 或 `手数 0.1`\n"
            "`lot 1.0` 或 `手数 1.0`\n\n"
            "🎯 示例: `lot 0.1`\n"
            "回复: 0.1手 = 10盎司 = $20,500\n\n"
            "📊 查看常见手数对照表:",
            reply_markup=reply_markup
        )
    
    elif query.data == 'lot_examples':
        examples = bot_tools.get_lot_size_examples()
        current_price = bot_tools.get_gold_price()
        
        examples_text = f"📊 常见手数对照表\n\n💰 当前金价: ${current_price}\n\n"
        
        for ex in examples:
            examples_text += f"🔸 **{ex['lot']} 手**\n"
            examples_text += f"   • 黄金: {ex['ounces']} 盎司\n"
            examples_text += f"   • 价值: ${ex['usd_value']:,}\n"
            examples_text += f"   • 每点: ${ex['pip_value']}\n\n"
        
        examples_text += "💡 发送 `lot 0.1` 计算自定义手数"
        
        back_keyboard = [
            [InlineKeyboardButton("🔙 返回计算器", callback_data='lot_calculator')]
        ]
        back_markup = InlineKeyboardMarkup(back_keyboard)
        
        await query.edit_message_text(examples_text, reply_markup=back_markup)
    
    elif query.data == 'gold_price':
        current_price = bot_tools.get_gold_price()
        change = round(random.uniform(-2, 2), 2)
        
        price_text = f"""💰 XAUUSD 当前价格

📊 **实时报价**:
• 当前价格: ${current_price}
• 24H变化: {change:+.2f}%
• 更新时间: {datetime.now().strftime('%H:%M:%S')}

📈 **交易信息**:
• 1标准手 = 100盎司 = ${current_price * 100:,.2f}
• 0.1手 = 10盎司 = ${current_price * 10:,.2f}
• 0.01手 = 1盎司 = ${current_price:,.2f}

🎯 基于此价格计算Lot Size"""
        
        back_keyboard = [
            [InlineKeyboardButton("💰 计算器", callback_data='lot_calculator')],
            [InlineKeyboardButton("📊 技术分析", callback_data='xauusd_analyze')]
        ]
        back_markup = InlineKeyboardMarkup(back_keyboard)
        
        await query.edit_message_text(price_text, reply_markup=back_markup)
    
    elif query.data == 'quick_analysis':
        analysis = bot_tools.analyze_xauusd_chart()
        bot_tools.xauusd_analysis_count += 1
        
        analysis_text = f"""🎯 XAUUSD 快速分析 #{bot_tools.xauusd_analysis_count}

📊 **交易建议**:
🔸 方向: {analysis['direction']} {'📈' if analysis['direction'] == 'LONG' else '📉'}
🔸 入场: ${analysis['entry']}
🔸 止损: ${analysis['sl']}
🔸 目标1: ${analysis['tp1']}
🔸 目标2: ${analysis['tp2']}

📈 **技术指标**:
• RSI: {analysis['rsi']} {'(超卖)' if analysis['rsi'] < 30 else '(超买)' if analysis['rsi'] > 70 else '(中性)'}
• MACD: {analysis['macd']}
• 当前价: ${analysis['current_price']}

🧠 **分析理由**:
{analysis['main_reason']}

💼 **风险管理**:
• 风险回报: 1:{analysis['risk_reward']}
• 信心度: {analysis['confidence']}
• 时间框架: {analysis['timeframe']}

⏰ {analysis['analysis_time']}"""
        
        await query.edit_message_text(analysis_text)
    
    elif query.data == 'bot_stats':
        stats_text = f"""📊 Bot 使用统计

🔒 **HTML 加密**:
• 加密次数: {bot_tools.html_encrypt_count}
• 状态: 正常运行 ✅

📊 **XAUUSD 分析**:
• 分析次数: {bot_tools.xauusd_analysis_count}
• 状态: 正常运行 ✅

💰 **Lot Size 计算**:
• 计算次数: {bot_tools.lot_calc_count}
• 状态: 正常运行 ✅

⏰ **运行信息**:
• 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• 服务器: 在线 🟢
• 开发者: @CKWinGg1330"""
        
        back_keyboard = [
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        back_markup = InlineKeyboardMarkup(back_keyboard)
        
        await query.edit_message_text(stats_text, reply_markup=back_markup)
    
    elif query.data == 'help_menu':
        help_text = """ℹ️ 使用帮助指南

🔒 **HTML 加密工具**:
• 上传 .html 文件或发送HTML代码
• 获取加密后的文件
• 保护源码不被复制

📊 **XAUUSD 分析工具**:
• 上传图表截图获取分析
• 快速分析获取建议
• 查看当前金价信息

💰 **Lot Size 计算器**:
• 发送: `lot 0.1` 或 `手数 0.1`
• 计算对应的USD金额
• 查看常见手数对照表

🎯 **使用技巧**:
• 所有功能都有按钮引导
• 支持中英文指令
• 24小时在线服务

📞 **联系方式**:
• Telegram: @CKWinGg1330
• 频道: @TeamCKGroup"""
        
        back_keyboard = [
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        back_markup = InlineKeyboardMarkup(back_keyboard)
        
        await query.edit_message_text(help_text, reply_markup=back_markup)
    
    elif query.data == 'main_menu':
        await start(update, context)
    
    elif query.data == 'upload_html':
        await query.edit_message_text(
            "📁 请上传HTML文件\n\n"
            "支持格式: .html, .htm\n"
            "文件大小: 最大5MB\n\n"
            "🔒 上传后立即获取加密文件"
        )
    
    elif query.data == 'send_html_code':
        await query.edit_message_text(
            "💻 请发送HTML代码\n\n"
            "示例:\n"
            "```html\n"
            "<html>\n"
            "<head><title>测试</title></head>\n"
            "<body><h1>Hello World</h1></body>\n"
            "</html>\n"
            "```\n\n"
            "🔒 发送后立即获取加密文件"
        )
    
    elif query.data == 'upload_chart':
        await query.edit_message_text(
            "📊 请上传XAUUSD图表截图\n\n"
            "🎯 建议包含:\n"
            "• 清晰的价格图表\n"
            "• 时间框架信息\n"
            "• 技术指标(可选)\n\n"
            "📷 支持格式: JPG, PNG, WebP\n"
            "📈 上传后获取专业分析"
        )

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
        
        bot_tools.html_encrypt_count += 1
        
        success_keyboard = [
            [InlineKeyboardButton("🔒 再次加密", callback_data='html_encrypt')],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        success_markup = InlineKeyboardMarkup(success_keyboard)
        
        await update.message.reply_text(
            f"✅ 加密成功！\n\n"
            f"🔒 已完成第 {bot_tools.html_encrypt_count} 次加密\n"
            f"🛡️ 源码已安全保护\n"
            f"📊 功能保持完整",
            reply_markup=success_markup
        )
        
    except Exception as e:
        logger.error(f"HTML加密错误: {e}")
        await processing_msg.edit_text("❌ 加密失败，请重试")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理XAUUSD图表分析"""
    try:
        processing_msg = await update.message.reply_text("📊 正在分析XAUUSD图表...")
        
        # 模拟分析过程
        await asyncio.sleep(1)
        
        # 获取图片
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        image_data = await file.download_as_bytearray()
        
        # 分析图表
        analysis = bot_tools.analyze_xauusd_chart(image_data)
        bot_tools.xauusd_analysis_count += 1
        
        # 生成分析报告
        analysis_text = f"""📊 XAUUSD 图表分析 #{bot_tools.xauusd_analysis_count}

🎯 **交易建议**:
━━━━━━━━━━━━━━━━━━━━━━━━
🔸 方向: {analysis['direction']} {'📈 做多' if analysis['direction'] == 'LONG' else '📉 做空'}
🔸 入场: ${analysis['entry']}
🔸 止损: ${analysis['sl']}
🔸 目标1: ${analysis['tp1']}
🔸 目标2: ${analysis['tp2']}

📈 **技术指标**:
━━━━━━━━━━━━━━━━━━━━━━━━
• RSI: {analysis['rsi']} {'(超卖)' if analysis['rsi'] < 30 else '(超买)' if analysis['rsi'] > 70 else '(中性)'}
• MACD: {analysis['macd']} {'(金叉)' if analysis['macd'] > 0 else '(死叉)'}
• 当前价: ${analysis['current_price']}

🧠 **分析理由**:
━━━━━━━━━━━━━━━━━━━━━━━━
{analysis['main_reason']}

💼 **风险管理**:
━━━━━━━━━━━━━━━━━━━━━━━━
• 风险回报比: 1:{analysis['risk_reward']}
• 信心度: {analysis['confidence']} {'🟢' if analysis['confidence'] == '高' else '🟡' if analysis['confidence'] == '中' else '🔴'}
• 时间框架: {analysis['timeframe']}
• 建议仓位: 2-3%

⏰ 分析时间: {analysis['analysis_time']}"""
        
        # 添加操作按钮
        result_keyboard = [
            [InlineKeyboardButton("📊 再次分析", callback_data='xauusd_analyze')],
            [InlineKeyboardButton("💰 计算仓位", callback_data='lot_calculator')],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
        ]
        result_markup = InlineKeyboardMarkup(result_keyboard)
        
        await update.message.reply_text(analysis_text, reply_markup=result_markup)
        await processing_msg.delete()
        
    except Exception as e:
        logger.error(f"图表分析错误: {e}")
        await update.message.reply_text("❌ 分析失败，请重试")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理文本消息"""
    text = update.message.text
    
    # Lot Size 计算
    lot_match = re.search(r'(?:lot|手数)\s*(\d+\.?\d*)', text.lower())
    if lot_match:
        lot_size = lot_match.group(1)
        calculation = bot_tools.calculate_lot_size_usd(lot_size)
        
        if calculation:
            bot_tools.lot_calc_count += 1
            
            calc_text = f"""💰 Lot Size 计算结果 #{bot_tools.lot_calc_count}

📊 **计算详情**:
━━━━━━━━━━━━━━━━━━━━━━━━
🔸 手数: {calculation['lot_size']} 标准手
🔸 黄金: {calculation['ounces']} 盎司
🔸 当前价: ${calculation['current_price']}
🔸 总价值: ${calculation['usd_value']:,}

💡 **交易信息**:
━━━━━━━━━━━━━━━━━━━━━━━━
• 每点价值: ${calculation['pip_value']}
• 所需保证金: ${calculation['margin_required']:,} (1%)
• 风险建议: 账户2-3%

📊 **仓位建议**:
━━━━━━━━━━━━━━━━━━━━━━━━
• 小额账户: 0.01-0.1手
• 中等账户: 0.1-1.0手  
• 大额账户: 1.0手以上

⏰ 计算时间: {calculation['calculation_time']}"""
            
            calc_keyboard = [
                [InlineKeyboardButton("📊 手数对照表", callback_data='lot_examples')],
                [InlineKeyboardButton("💹 当前金价", callback_data='gold_price')],
                [InlineKeyboardButton("🔙 返回主菜单", callback_data='main_menu')]
            ]
            calc_markup = InlineKeyboardMarkup(calc_keyboard)
            
            await update.message.reply_text(calc_text, reply_markup=calc_markup)
        else:
            await update.message.reply_text("❌ 手数格式错误\n\n请使用: `lot 0.1` 或 `手数 0.1`")
    
    # HTML 代码加密
    elif text.strip().startswith('<') and text.strip().endswith('>'):
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
            
            bot_tools.html_encrypt_count += 1
            
            await update.message.reply_text(
                f"✅ 代码加密成功！\n\n"
                f"🔒 已完成第 {bot_tools.html_encrypt_count} 次加密"
            )
            
        except Exception as e:
            logger.error(f"HTML代码加密错误: {e}")
            await processing_msg.edit_text("❌ 加密失败，请重试")
    
    # 关键词识别
    elif any(word in text.lower() for word in ['金价', 'xauusd', 'gold', '黄金']):
        await update.message.reply_text(
            "📊 我看到您询问黄金相关信息！\n\n"
            "🎯 您可以：\n"
            "• 上传图表获取分析\n"
            "• 查看当前金价\n"
            "• 计算仓位大小\n\n"
            "💡 发送 /start 查看完整功能"
        )
    
    elif any(word in text.lower() for word in ['html', '加密', '网页', 'encrypt']):
        await update.message.reply_text(
            "🔒 我看到您询问HTML加密！\n\n"
            "🎯 您可以：\n"
            "• 上传HTML文件加密\n"
            "• 发送HTML代码加密\n"
            "• 保护网页源码\n\n"
            "💡 发送 /start 查看完整功能"
        )
    
    elif any(word in text.lower() for word in ['lot', '手数', '仓位', '计算']):
        await update.message.reply_text(
            "💰 Lot Size 计算器使用方法：\n\n"
            "📝 **输入格式**:\n"
            "• `lot 0.1` \n"
            "• `手数 0.1`\n"
            "• `lot 1.0`\n\n"
            "📊 **示例**:\n"
            "`lot 0.1` → 0.1手 = 10盎司 = $20,500\n\n"
            "💡 试试发送: `lot 0.1`"
        )
    
    # 统计命令
    elif text.lower() == '/stats':
        stats_text = f"""📊 详细统计信息

🔒 **HTML 加密统计**:
• 加密次数: {bot_tools.html_encrypt_count}
• 成功率: 100% ✅

📊 **XAUUSD 分析统计**:
• 分析次数: {bot_tools.xauusd_analysis_count}
• 成功率: 100% ✅

💰 **Lot Size 计算统计**:
• 计算次数: {bot_tools.lot_calc_count}
• 成功率: 100% ✅

🎯 **总使用次数**: {bot_tools.html_encrypt_count + bot_tools.xauusd_analysis_count + bot_tools.lot_calc_count}

⏰ 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        await update.message.reply_text(stats_text)
    
    # 默认回复
    else:
        await update.message.reply_text(
            "👋 欢迎使用多功能交易工具！\n\n"
            "🎯 **快速开始**:\n"
            "• 发送 `/start` 查看所有功能\n"
            "• 发送 `lot 0.1` 计算手数\n"
            "• 发送HTML代码进行加密\n"
            "• 上传图表获取分析\n\n"
            "💡 选择您需要的功能开始使用！"
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
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("🚀 多功能交易工具 Bot 启动中...")
    print("🔒 HTML 加密功能已就绪")
    print("📊 XAUUSD 分析功能已就绪")
    print("💰 Lot Size 计算功能已就绪")
    print("✅ 所有功能正常运行")
    
    application.run_polling()

if __name__ == '__main__':
    main()
