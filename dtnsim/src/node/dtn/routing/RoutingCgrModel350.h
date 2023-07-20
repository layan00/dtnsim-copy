
#ifndef SRC_NODE_DTN_ROUTINGCGRMODEL_H_
#define SRC_NODE_DTN_ROUTINGCGRMODEL_H_

#include <src/node/dtn/routing/CgrRoute.h>
#include <src/node/dtn/routing/RoutingDeterministic.h>
#include <src/node/dtn/SdrModel.h>
#include <src/node/dtn/routing/RoutingInterRegions.h>

class RoutingCgrModel350: public RoutingDeterministic
{
public:
	RoutingCgrModel350(int eid, SdrModel * sdr, map<string, ContactPlan> *contactPlans, RoutingInterRegions *routingInterRegions, bool printDebug);
	virtual ~RoutingCgrModel350();
	virtual void routeAndQueueBundle(BundlePkt *bundle, double simTime, int terminusNode);
	virtual CgrRoute* getCgrBestRoute(BundlePkt * bundle, double simTime);
	virtual vector<CgrRoute> getCgrRoutes(BundlePkt * bundle, double simTime);


	// stats recollection
	double getDijkstraCalls();
	double getDijkstraLoops();
	double getRouteTableEntriesExplored();
	double getEdgesOneDijkstra() const;
	double getNodesOneDijkstra() const;
	double getOneDijkstraComplexity() const;
	double getRouteTableSize();

private:

	double dijkstraCalls;
	double dijkstraLoops;
	double tableEntriesExplored;
	double routeTableSize;

	double nodesOneDijkstra;
	double edgesOneDijkstra;


	bool printDebug_ = false;

	/////////////////////////////////////////////////
	// Ion Cgr Functions based in libcgr.c (v 3.5.0):
	/////////////////////////////////////////////////
#define	MIN_CONFIDENCE_IMPROVEMENT	(.05)
#define MIN_DTN_DELIVERY_CONFIDENCE	(.80)
#define MAX_XMIT_COPIES (20)
#define	MAX_SPEED_MPH	(150000)

	typedef struct
	{
		int neighborNodeNbr;
		int contactId; // This is not, in ION
		double forfeitTime;
		double arrivalTime;
		float confidence;
		unsigned int hopCount; // hops from dest. node.
		CgrRoute * route; // pointer to route so we can decrement capacities
		//Scalar	overbooked; 	//Bytes needing reforward.
		//Scalar	protected; 		//Bytes not overbooked.
	} ProximateNode;

	typedef struct
	{
		Contact * contact;
		Contact * predecessor;	// predecessor Contact
		double arrivalTime;
		double capacity; 	// in Bytes
		bool visited;
		bool suppressed;
	} Work;

	map<string, map<int, vector<CgrRoute> > >routeLists_;

	map<string, double> routeListLastEditTimes_;

	void cgrForward(BundlePkt * bundle, double simTime, int terminusNode);
	void identifyProximateNodes(BundlePkt * bundle, double simTime, int terminusNode, vector<int> excludedNodes, vector<ProximateNode> * proximateNodes);
	void loadRouteList(int terminusNode, double simTime);

	void findNextBestRoute(Contact * rootContact, int terminusNode, CgrRoute * route);
	void tryRoute(BundlePkt * bundle, CgrRoute * route, vector<ProximateNode> * proximateNodes);
	void recomputeRouteForContact();
	void enqueueToNeighbor(BundlePkt * bundle, ProximateNode * selectedNeighbor);
	void enqueueToLimbo(BundlePkt * bundle);
	void bpEnqueue(BundlePkt * bundle, ProximateNode * selectedNeighbor);
};

#endif /* SRC_NODE_DTN_ROUTINGCGRMODEL_H_ */
