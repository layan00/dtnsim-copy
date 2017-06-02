#include <dtn/ContactPlan.h>

ContactPlan::~ContactPlan() {

}

ContactPlan::ContactPlan() {

}

void ContactPlan::parseContactPlanFile(string fileName) {
	int id = 1;
	double start = 0.0;
	double end = 0.0;
	int sourceEid = 0;
	int destinationEid = 0;
	double dataRateOrRange = 0.0;

	string fileLine = "#";
	string a;
	string command;
	ifstream file;

	file.open(fileName.c_str());

	if (!file.is_open())
		throw cException(("Error: wrong path to contacts file " + string(fileName)).c_str());

	while (getline(file, fileLine)) {
		if (fileLine.empty())
			continue;

		if (fileLine.at(0) == '#')
			continue;

		// This seems to be a valid command line, parse it
		stringstream stringLine(fileLine);
		stringLine >> a >> command >> start >> end >> sourceEid >> destinationEid >> dataRateOrRange;

		if (a.compare("a") == 0) {
			if ((command.compare("contact") == 0)) {
				this->addContact(id, start, end, sourceEid, destinationEid, dataRateOrRange, (float) 1.0);
				id++;
			} else if ((command.compare("range") == 0)) {
				this->addRange(id, start, end, sourceEid, destinationEid, dataRateOrRange, (float) 1.0);
				id++;
			} else {
				cout << "dtnsim error: unknown contact plan command type: a " << fileLine << endl;
			}
		}
	}

	if (cin.bad()) {
		// IO error
	} else if (!cin.eof()) {
		// format error (not possible with getline but possible with operator>>)
	} else {
		// format error (not possible with getline but possible with operator>>)
		// or end of file (can't make the difference)
	}

	file.close();

	this->setContactsFile(fileName);
	this->finishContactPlan();
}

void ContactPlan::addContact(int id, double start, double end, int sourceEid, int destinationEid, double dataRate,
		float confidence) {
	Contact contact(id, start, end, sourceEid, destinationEid, dataRate, confidence);

	contacts_.push_back(contact);

	lastEditTime = simTime();
}

void ContactPlan::addRange(int id, double start, double end, int sourceEid, int destinationEid, double range,
		float confidence) {

	// Ranges can be declared in a single direction, but they are bidirectional
	Contact contact1(id, start, end, sourceEid, destinationEid, range, confidence);
	Contact contact2(id, start, end, destinationEid, sourceEid, range, confidence);

	ranges_.push_back(contact1);
	ranges_.push_back(contact2);

	lastEditTime = simTime();
}

double ContactPlan::getRangeBySrcDst(int Src, int Dst) {
	vector<Contact> ranges;
	vector<Contact *> rangesSrcDst;
	vector<Contact *> rangesSrc;

	cout << Src << " " << Dst << endl;

	map<int, vector<Contact *> >::iterator it = rangesBySrc_.find(Src);

	if (it != rangesBySrc_.end()) {
		rangesSrc = it->second;
	}

	for (size_t i = 0; i < rangesSrc.size(); i++) {
		if (rangesSrc.at(i)->getDestinationEid() == Dst) {
			rangesSrcDst.push_back(rangesSrc.at(i));
		}
	}

	for (size_t i = 0; i < rangesSrcDst.size(); i++) {
		ranges.push_back(*rangesSrcDst.at(i));
	}

	if (!ranges.empty())
		return ranges.at(0).getDataRate();
	else
		return -1;
}

void ContactPlan::finishContactPlan() {
	for (size_t i = 0; i < contacts_.size(); i++) {
		Contact *contactPtr = &contacts_.at(i);

		contactsBySrc_[contactPtr->getSourceEid()].push_back(contactPtr);
		contactsByDst_[contactPtr->getDestinationEid()].push_back(contactPtr);
		contactsById_[contactPtr->getId()] = contactPtr;
	}

	for (size_t i = 0; i < ranges_.size(); i++) {
		Contact *contactPtr = &ranges_.at(i);

		rangesBySrc_[contactPtr->getSourceEid()].push_back(contactPtr);
		rangesByDst_[contactPtr->getDestinationEid()].push_back(contactPtr);
		rangesById_[contactPtr->getId()] = contactPtr;
	}
}

Contact *ContactPlan::getContactById(int id) {
	Contact *contactPtr = NULL;

	map<int, Contact *>::iterator it = contactsById_.find(id);
	if (it != contactsById_.end()) {
		contactPtr = it->second;
	}

	return contactPtr;
}

vector<Contact> * ContactPlan::getContacts() {
	return &contacts_;
}

vector<Contact> ContactPlan::getContactsBySrc(int Src) {
	vector<Contact> contacts;
	map<int, vector<Contact *> >::iterator it = contactsBySrc_.find(Src);

	if (it != contactsBySrc_.end()) {
		vector<Contact *> contactsPtr = it->second;
		for (size_t i = 0; i < contactsPtr.size(); i++) {
			contacts.push_back(*contactsPtr.at(i));
		}
	}

	return contacts;
}

vector<Contact> ContactPlan::getContactsByDst(int Dst) {
	vector<Contact> contacts;
	map<int, vector<Contact *> >::iterator it = contactsByDst_.find(Dst);

	if (it != contactsByDst_.end()) {
		vector<Contact *> contactsPtr = it->second;
		for (size_t i = 0; i < contactsPtr.size(); i++) {
			contacts.push_back(*contactsPtr.at(i));
		}
	}

	return contacts;
}

vector<Contact> ContactPlan::getContactsBySrcDst(int Src, int Dst) {
	vector<Contact> contacts;
	vector<Contact *> contactsSrcDst;
	vector<Contact *> contactsSrc;

	map<int, vector<Contact *> >::iterator it = contactsBySrc_.find(Src);

	if (it != contactsBySrc_.end()) {
		contactsSrc = it->second;
	}

	for (size_t i = 0; i < contactsSrc.size(); i++) {
		if (contactsSrc.at(i)->getDestinationEid() == Dst) {
			contactsSrcDst.push_back(contactsSrc.at(i));
		}
	}

	for (size_t i = 0; i < contactsSrcDst.size(); i++) {
		contacts.push_back(*contactsSrcDst.at(i));
	}

	return contacts;
}

simtime_t ContactPlan::getLastEditTime() {
	return lastEditTime;
}

Contact ContactPlan::getContactByTuple(int src, int dst, double start, double end) {
	Contact contactByTuple(0, 0, 0, 0, 0, 0, 0);
	vector<Contact> contacts = getContactsBySrcDst(src, dst);
	for (size_t i = 0; i < contacts.size(); i++) {
		if ((contacts.at(i).getSourceEid() != src) || (contacts.at(i).getDestinationEid() != dst)) {
			cout << "Error in method getContactsBySrcDst" << endl;
		}

		if ((contacts.at(i).getStart() == start) && (contacts.at(i).getEnd() == end)) {
			contactByTuple = contacts.at(i);
			break;
		}
	}

	return contactByTuple;
}

void ContactPlan::setContactsFile(string contactsFile) {
	contactsFile_ = contactsFile;
}

const string& ContactPlan::getContactsFile() const {
	return contactsFile_;
}

void ContactPlan::printContactPlan() {
	vector<Contact>::iterator it;
	for (it = this->getContacts()->begin(); it != this->getContacts()->end(); ++it)
		cout << "a contact +" << (*it).getStart() << " +" << (*it).getEnd() << " " << (*it).getSourceEid() << " "
				<< (*it).getDestinationEid() << " " << (*it).getResidualVolume() << "/" << (*it).getVolume() << endl;
	cout << endl;
}
