"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const axios_1 = __importDefault(require("axios"));
const encode = async () => {
    const response = await axios_1.default.post('https://yincrypt.vercel.app/api/encode', {
        "type": "base64",
        "text": "ayiinxd"
    }, {
        headers: {
            "Content-Type": "application/json"
        }
    });
    const result = response.data;
    console.log(result); // output: YXlpaW54ZA==
};
const decode = async () => {
    const response = await axios_1.default.post('https://yincrypt.vercel.app/api/decode', {
        "type": "base64",
        "text": "YXlpaW54ZA=="
    }, {
        headers: {
            "Content-Type": "application/json"
        }
    });
    const result = response.data;
    console.log(result); // output: ayiinxd
};
(async () => {
    console.log("Running Encode And Decode");
    encode();
    decode();
    console.log("Ended Encode Anda Decode");
})();
//# sourceMappingURL=index.js.map