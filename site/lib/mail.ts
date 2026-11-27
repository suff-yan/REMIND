import nodemailer from "nodemailer";

export async function sendMail(to: string, subject: string, text: string) {
  const { SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, MAIL_FROM, MAIL_REPLY_TO } = process.env;
  if (!SMTP_HOST || !SMTP_USER || !SMTP_PASS) {
    console.log(`[mail disabled] to=${to} subject=${subject}\n${text}`);
    return false;
  }
  const port = Number(SMTP_PORT || 465);
  const t = nodemailer.createTransport({ host: SMTP_HOST, port, secure: port === 465, auth: { user: SMTP_USER, pass: SMTP_PASS } });
  await t.sendMail({ from: MAIL_FROM || SMTP_USER, replyTo: MAIL_REPLY_TO || undefined, to, subject, text });
  return true;
}
