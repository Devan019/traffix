import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class Message {
  final String text;
  final bool fromUser;
  final DateTime time;

  Message({required this.text, required this.fromUser}) : time = DateTime.now();
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await dotenv.load(fileName: ".env");

  runApp(TraffixChatApp());
}
class TraffixChatApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Traffix Bot',
      theme: ThemeData(primarySwatch: Colors.indigo),
      home: ChatScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class ChatScreen extends StatefulWidget {
  @override
  State createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<Message> _messages = [];
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  bool botTyping = false;

  // ----------- API CALL TO FASTAPI BACKEND -------------
  Future<String> sendQueryToBot(String query) async {
    final url = Uri.parse("http://localhost:8000/traffic-query");

    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"query": query}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data["response"];
    } else {
      return "Server error: Please try again later.";
    }
  }

  // ----------- SEND MESSAGE --------------
  void _sendMessage() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _messages.add(Message(text: text, fromUser: true));
      botTyping = true;
    });

    _controller.clear();
    _scrollToBottom();

    // API Call
    final botReply = await sendQueryToBot(text);

    setState(() {
      botTyping = false;
      _messages.add(Message(text: botReply, fromUser: false));
    });

    _scrollToBottom();
  }

  // ----------- SCROLL TO BOTTOM ----------
  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!_scrollController.hasClients) return;
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent + 60,
        duration: Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    });
  }

  // ----------- MESSAGE BUBBLE UI ----------
  Widget _buildMessageTile(Message m) {
    final align = m.fromUser
        ? CrossAxisAlignment.end
        : CrossAxisAlignment.start;
    final bgColor = m.fromUser ? Colors.indigo : Colors.grey.shade200;
    final textColor = m.fromUser ? Colors.white : Colors.black87;

    final radius = m.fromUser
        ? BorderRadius.only(
            topLeft: Radius.circular(16),
            topRight: Radius.circular(16),
            bottomLeft: Radius.circular(16),
          )
        : BorderRadius.only(
            topLeft: Radius.circular(16),
            topRight: Radius.circular(16),
            bottomRight: Radius.circular(16),
          );

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: Column(
        crossAxisAlignment: align,
        children: [
          Container(
            constraints: BoxConstraints(
              maxWidth: MediaQuery.of(context).size.width * 0.78,
            ),
            padding: EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            decoration: BoxDecoration(color: bgColor, borderRadius: radius),
            child: m.fromUser
                ? Text(
                    m.text.replaceAll("\\n", "\n"),
                    style: TextStyle(
                      color: textColor,
                      fontSize: 15,
                      height: 1.35,
                    ),
                  )
                : MarkdownBody(
                    data: m.text.replaceAll("\\n", "\n"),
                    styleSheet: MarkdownStyleSheet.fromTheme(Theme.of(context))
                        .copyWith(
                          p: TextStyle(
                            color: textColor,
                            fontSize: 15,
                            height: 1.35,
                          ),
                          strong: TextStyle(
                            color: textColor,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                  ),
          ),
          SizedBox(height: 4),
          Text(
            "${m.time.hour.toString().padLeft(2, '0')}:${m.time.minute.toString().padLeft(2, '0')}",
            style: TextStyle(fontSize: 11, color: Colors.black45),
          ),
        ],
      ),
    );
  }

  // -------------------------------------------------------

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            CircleAvatar(child: Icon(Icons.directions_car, size: 18)),
            SizedBox(width: 10),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("Traffix Bot", style: TextStyle(fontSize: 16)),
                Text("Traffic Law Assistant", style: TextStyle(fontSize: 12)),
              ],
            ),
          ],
        ),
      ),

      body: SafeArea(
        child: Column(
          children: [
            // -------- Chat Messages --------
            Expanded(
              child: ListView.builder(
                controller: _scrollController,
                padding: EdgeInsets.symmetric(vertical: 12),
                itemCount: _messages.length,
                itemBuilder: (context, index) =>
                    _buildMessageTile(_messages[index]),
              ),
            ),

            if (botTyping)
              Padding(
                padding: EdgeInsets.only(left: 16, bottom: 6),
                child: Row(
                  children: [
                    CircularProgressIndicator(strokeWidth: 2),
                    SizedBox(width: 12),
                    Text("Bot is typing..."),
                  ],
                ),
              ),

            Divider(height: 1),

            // -------- Input Field --------
            Container(
              color: Colors.white,
              padding: EdgeInsets.symmetric(horizontal: 8, vertical: 6),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      textInputAction: TextInputAction.send,
                      onSubmitted: (_) => _sendMessage(),
                      decoration: InputDecoration(
                        hintText: "Ask about traffic laws...",
                        filled: true,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(24),
                          borderSide: BorderSide.none,
                        ),
                        contentPadding: EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 12,
                        ),
                      ),
                    ),
                  ),

                  SizedBox(width: 8),

                  GestureDetector(
                    onTap: _sendMessage,
                    child: CircleAvatar(
                      radius: 22,
                      backgroundColor: Colors.indigo,
                      child: Icon(Icons.send, color: Colors.white),
                    ),
                  ),
                ],
              ),
            ),
            SizedBox(height: 6),
          ],
        ),
      ),
    );
  }
}
