import pytest
from unittest.mock import AsyncMock, patch
from discord_bot.main import CI_notificator

@pytest.fixture
def bot():
    bot = CI_notificator()
    return bot

# Test the send_notification method
# Ensure the bot sends a message to the correct channel
# Ensure the bot sends the correct message
@pytest.mark.asyncio
async def test_send_notification(bot):
    # Mock the get_channel method to return a mock channel with an async send method
    with patch.object(bot.bot, "get_channel", return_value=AsyncMock(send=AsyncMock())) as mock_get_channel:
        await bot.send_notification("Test message")
        # Ensure get_channel was called with the correct channel ID
        mock_get_channel.assert_called_once_with(1205521583095947264)
        # Ensure the send method was called on the channel with the correct message
        mock_get_channel.return_value.send.assert_awaited_once_with("Test message")
