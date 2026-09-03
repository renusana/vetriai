import emailjs from "@emailjs/browser";

const SERVICE_ID = "service_6lw1qoo";
const TEMPLATE_ID = "template_xdyxtlm";
const PUBLIC_KEY = "q9dvDM5rSw8yNKYSL";

export const sendNotificationEmail = async ({
    to_name,
    to_email,
    message,
    notification_type,
    notification_time,
}) => {
    try {
        const templateParams = {
            to_name,
            to_email,
            message,
            notification_type,
            notification_time,
        };

        const response = await emailjs.send(
            SERVICE_ID,
            TEMPLATE_ID,
            templateParams,
            PUBLIC_KEY
        );

        console.log("EmailJS success:", response);

        return {
            success: true,
            response,
        };
    } catch (error) {
        console.error("EmailJS error:", error);

        return {
            success: false,
            error,
        };
    }
};

