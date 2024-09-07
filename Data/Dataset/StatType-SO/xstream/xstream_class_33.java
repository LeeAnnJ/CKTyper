
// https://github.com/PortSwigger/amf-deserializer/blob/master/src/org/apache/jmeter/protocol/amf/util/AmfXmlConverter.java

public class xstream_class_33 {
	private static XStream xstream;

	public static XStream getXStream() {
		if (xstream == null) {
			xstream = new XStream(new DomDriver());

			xstream.alias("ActionMessage", ActionMessage.class);
			xstream.alias("MessageHeader", MessageHeader.class);
			xstream.alias("MessageBody", MessageBody.class);
			xstream.alias("RemotingMessage", RemotingMessage.class);
			xstream.alias("CommandMessage", CommandMessage.class);
			xstream.alias("AcknowledgeMessage", AcknowledgeMessage.class);
			xstream.alias("ErrorMessage", ErrorMessage.class);
			xstream.alias("ASObject", ASObject.class);
			xstream.alias("AsyncMessage", AsyncMessage.class);
			xstream.alias("DSC", CommandMessageExt.class);
			xstream.alias("DSK", AcknowledgeMessageExt.class);

			// Better ASObject Converter
			Mapper mapper = xstream.getMapper();
		}

		return xstream;
	}
}
