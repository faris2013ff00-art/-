
const {
    Client,
    GatewayIntentBits,
    PermissionsBitField
} = require("discord.js");

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMembers
    ]
});

// ==================================
// الكلمات الممنوعة
// ==================================

const badWords = [
    "قحبه",
    "ازغبك",
    "امك",
    "اركب عليه",
    "كس",
    "انيك",
    "انيكك",
    "امكك",
    "اني..ك",
    "طيزك",
    "زب",
    "زبك",
    "مكوتك",
    "جمل ابو راسين",
    "مص",
    "تنيك",
    "كس امك",
    "مزغوب",
    "قح.به",
    "يامفتوح"
];

// ==================================
// تنظيف النص من التشكيل والتحايل
// ==================================

function normalize(text) {
    return text
        .toLowerCase()
        .replace(/[\u064B-\u065F\u0670\u0640]/g, "")
        .replace(/[أإآٱ]/g, "ا")
        .replace(/ى/g, "ي")
        .replace(/[^\p{L}\p{N}]/gu, "");
}

const forbidden = badWords
    .map(word => normalize(word))
    .filter(Boolean);

// ==================================
// تشغيل البوت
// ==================================

client.once("ready", () => {
    console.log(`Bot is online: ${client.user.tag}`);
});

// ==================================
// مراقبة الرسائل
// ==================================

client.on("messageCreate", async (message) => {

    if (!message.guild || message.author.bot) return;

    const content = normalize(message.content);

    const found = forbidden.some(word =>
        content.includes(word)
    );

    if (!found) return;

    try {

        // حذف رسالة العضو فوراً
        await message.delete();

        // Timeout لمدة 10 ثوانٍ
        await message.member.timeout(
            10 * 1000,
            "استخدام كلمة ممنوعة"
        );

        console.log(
            `تم حذف رسالة ومعاقبة ${message.author.tag}`
        );

        // الانتظار حتى انتهاء العقوبة
        await new Promise(resolve =>
            setTimeout(resolve, 10 * 1000)
        );

        // إرسال التحذير بعد انتهاء العقوبة
        const warning = await message.channel.send({
            content: `⚠️ ${message.author} ممنوع تقول كلام بذيئ او قذف`
        });

        // حذف التحذير بعد 20 ثانية
        setTimeout(async () => {
            try {
                await warning.delete();
            } catch (error) {
                console.error("تعذر حذف التحذير:", error);
            }
        }, 20 * 1000);

    } catch (error) {

        console.error("Error:", error);

    }

});

// ==================================
// تسجيل الدخول
// ==================================

if (!process.env.DISCORD_TOKEN) {
    throw new Error("DISCORD_TOKEN غير موجود!");
}

client.login(process.env.DISCORD_TOKEN);
