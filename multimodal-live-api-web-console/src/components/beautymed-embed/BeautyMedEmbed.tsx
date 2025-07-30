/**
 * BeautyMed Clinic Voice Assistant Embed Component
 * Simplified voice agent specifically for BeautyMed clinic appointments
 */

import { useEffect, useState } from "react";
import { useLiveAPIContext } from "../../contexts/LiveAPIContext";
import AudioPulse from "../audio-pulse/AudioPulse";
import "./beautymed-embed.scss";

export default function BeautyMedEmbed() {
  const { client, connected, connect, disconnect, setConfig } = useLiveAPIContext();
  const [isConnecting, setIsConnecting] = useState(false);
  const [response, setResponse] = useState<string>('สวัสดีค่ะ! ยินดีต้อนรับสู่ BeautyMed Clinic ดิฉัน Robin ผู้ช่วยนัดหมาย พร้อมช่วยเหลือคุณค่ะ');

  // Configure for BeautyMed clinic
  useEffect(() => {
    setConfig({
      model: "models/gemini-2.0-flash-exp",
      systemInstruction: {
        parts: [
          {
            text: `คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic คลินิกความงาม 
            
            ตอบเป็นภาษาไทยเท่านั้น โดยใช้คำพูดที่สุภาพและเป็นมิตร
            
            หน้าที่ของคุณ:
            1. ต้อนรับผู้ป่วยด้วยความอบอุ่น
            2. ช่วยจองนัดหมายสำหรับบริการต่างๆ ของคลินิก
            3. แนะนำบริการความงามของคลินิก
            4. ตอบคำถามเกี่ยวกับการดูแลก่อนและหลังการรักษา
            5. สอบถามข้อมูลที่จำเป็นสำหรับการนัดหมาย
            
            บริการของคลินิก:
            - ฉีดโบท็อกซ์
            - ฟิลเลอร์
            - การรักษาสิว
            - เลเซอร์กำจัดขน
            - ฟอโตเฟเชียล
            - การดูแลผิวหน้า
            
            เวลาทำการ: จันทร์-เสาร์ 9:00-18:00
            
            ให้คำตอบสั้นๆ กระชับ และช่วยเหลือผู้ป่วยอย่างเต็มที่`
          },
        ],
      },
      generationConfig: {
        responseModalities: ["audio"],
        speechConfig: {
          voiceConfig: {
            prebuiltVoiceConfig: {
              voiceName: "Aoede", // Female voice
            }
          }
        }
      }
    });
  }, [setConfig]);

  // Handle responses
  useEffect(() => {
    const onResponse = (data: any) => {
      console.log("BeautyMed received response:", data);
      if (data.text) {
        setResponse(data.text);
      }
    };

    const onConnected = () => {
      setIsConnecting(false);
    };

    const onDisconnected = () => {
      setIsConnecting(false);
    };

    client.on("response", onResponse);
    client.on("connected", onConnected);
    client.on("disconnected", onDisconnected);
    
    return () => {
      client.off("response", onResponse);
      client.off("connected", onConnected);
      client.off("disconnected", onDisconnected);
    };
  }, [client]);

  const handleConnect = async () => {
    if (connected) {
      disconnect();
    } else {
      setIsConnecting(true);
      try {
        await connect();
      } catch (error) {
        console.error("Connection error:", error);
        setIsConnecting(false);
      }
    }
  };

  const sendMessage = (text: string) => {
    if (connected) {
      client.send(text);
    }
  };

  return (
    <div className="beautymed-embed">
      {/* Header */}
      <div className="embed-header">
        <div className="clinic-logo">
          💄 BeautyMed Clinic
        </div>
        <div className="status-indicator">
          <span className={`status-dot ${connected ? 'connected' : 'disconnected'}`}></span>
          {connected ? 'เชื่อมต่อแล้ว' : 'ยังไม่ได้เชื่อมต่อ'}
        </div>
      </div>

      {/* Voice Controls */}
      <div className="voice-controls">
        <button
          className={`record-button ${connected ? 'connected' : ''} ${isConnecting ? 'connecting' : ''}`}
          onClick={handleConnect}
          disabled={isConnecting}
        >
          {isConnecting ? (
            <>
              <div className="spinner"></div>
              กำลังเชื่อมต่อ...
            </>
          ) : connected ? (
            <>
              <AudioPulse />
              🎙️ พูดได้เลย
            </>
          ) : (
            <>
              🎤 เชื่อมต่อเพื่อเริ่มพูด
            </>
          )}
        </button>
      </div>

      {/* Response Display */}
      {response && (
        <div className="response-display">
          <div className="assistant-name">Robin:</div>
          <div className="response-text">{response}</div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="quick-actions">
        <button 
          className="quick-action-btn"
          onClick={() => sendMessage("ขอนัดหมายฉีดโบท็อกซ์ค่ะ")}
          disabled={!connected}
        >
          จองนัดโบท็อกซ์
        </button>
        <button 
          className="quick-action-btn"
          onClick={() => sendMessage("อยากสอบถามเรื่องฟิลเลอร์ค่ะ")}
          disabled={!connected}
        >
          ถามเรื่องฟิลเลอร์
        </button>
        <button 
          className="quick-action-btn"
          onClick={() => sendMessage("ราคาบริการเท่าไหร่ค่ะ")}
          disabled={!connected}
        >
          สอบถามราคา
        </button>
      </div>

      {/* Footer */}
      <div className="embed-footer">
        🕒 เวลาทำการ: จันทร์-เสาร์ 9:00-18:00
      </div>
    </div>
  );
}